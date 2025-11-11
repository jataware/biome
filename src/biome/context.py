import os
import re
import logging
import json
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict

from beaker_kernel.lib.context import BeakerContext
from beaker_kernel.subkernels.python import PythonSubkernel

from .agent import BiomeAgent
from .integrations import BiomeAdhocIntegrations


if TYPE_CHECKING:
    from beaker_kernel.kernel import LLMKernel
    from beaker_kernel.lib.agent import BaseAgent


logger = logging.getLogger(__name__)


class BiomeContext(BeakerContext):
    SLUG = "biome"
    DISPLAY_NAME = "Biomedical"
    agent_cls: "BaseAgent" = BiomeAgent

    def __init__(self, beaker_kernel: "LLMKernel", config: Dict[str, Any]):
        from adhoc_api.uaii import gpt_41, o3_mini, claude_37_sonnet, gemini_15_pro
        ttl_seconds = 1800
        drafter_config_gemini = {**gemini_15_pro, 'ttl_seconds': ttl_seconds, 'api_key': os.environ.get("GEMINI_API_KEY", "")}
        drafter_config_anthropic = {**claude_37_sonnet, 'api_key': os.environ.get("ANTHROPIC_API_KEY")}
        curator_config = {**o3_mini, 'api_key': os.environ.get("OPENAI_API_KEY")}
        gpt_41_config = {**gpt_41, 'api_key': os.environ.get("OPENAI_API_KEY")}

        # Initialize adhoc integration
        adhoc_integration = BiomeAdhocIntegrations(
            drafter_config=[gpt_41_config, drafter_config_anthropic, drafter_config_gemini],
            curator_config=curator_config,
            contextualizer_config=gpt_41_config,
            logger=logger,
            display_name="Specialist Agents"
        )

        # Track missing API keys (must be set before super().__init__ for agent access)
        self.api_key_map: Dict[str, str] = {
            "API_EPA_AQS": "EPA Air Quality System (air quality monitoring data)",
            "API_EPA_AQS_EMAIL": "EPA Air Quality System email (required for API access)",
            "API_OPENFDA": "OpenFDA (FDA adverse event reports and drug/device data)",
            "API_USDA_FDC": "USDA FoodData Central (nutritional and food composition data)",
            "API_CENSUS": "US Census Bureau API (demographic and economic data)",
            "API_CDC_TRACKING_NETWORK": "CDC Environmental Public Health Tracking Network",
            "API_SYNAPSE": "Sage Bionetworks Synapse (collaborative biomedical research platform)",
            "NETRIAS_KEY": "NETRIAS (clinical trials and genomic data)",
            "ALPHAGENOME_KEY": "AlphaGenome (genomic analysis and sequencing data)",
            "IMMPORT_USERNAME": "ImmPort username (Immunology Database and Analysis Portal)",
            "IMMPORT_PASSWORD": "ImmPort password (Immunology Database and Analysis Portal)",
            "ENTREZ_EMAIL": "NCBI Entrez email (required for PubMed and NCBI database access)",
            "ENTREZ_API_KEY": "NCBI Entrez API key (for higher rate limits on NCBI databases)"
        }
        self.missing_api_keys: Dict[str, str] = self._get_missing_api_keys()
        if self.missing_api_keys:
            logger.warning(f"Missing API keys: {', '.join(self.missing_api_keys.values())}")

        super().__init__(
            beaker_kernel,
            self.agent_cls,
            config,
            integrations=[adhoc_integration]
        )

        if not isinstance(self.subkernel, PythonSubkernel):
            raise ValueError("This context is only valid for Python.")

    def _get_missing_api_keys(self) -> Dict[str, str]:
        """Identify API keys that are missing or invalid."""
        def is_invalid(value: str) -> bool:
            return not value or value in ("None", "")

        return {
            env_var: name
            for env_var, name in self.api_key_map.items()
            if is_invalid(os.environ.get(env_var, ""))
        }

    async def setup(self, context_info=None, parent_header=None):
        """Run setup script to configure the environment."""
        command = self.get_code("setup", {
            "aqs_api_key": os.environ.get("API_EPA_AQS"),
            "aqs_email": os.environ.get("API_EPA_AQS_EMAIL"),
            "openfda_faers_api_key": os.environ.get("API_OPENFDA"),
            "usda_fdc_api_key": os.environ.get("API_USDA_FDC"),
            "census_api_key": os.environ.get("API_CENSUS"),
            "cdc_tracking_network_api_key": os.environ.get("API_CDC_TRACKING_NETWORK"),
            "synapse_api_key": os.environ.get("API_SYNAPSE"),
            "netrias_api_key": os.environ.get("NETRIAS_KEY"),
            "alphagenome_key": os.environ.get("ALPHAGENOME_KEY"),
            "immport_username": os.environ.get("IMMPORT_USERNAME"),
            "immport_password": os.environ.get("IMMPORT_PASSWORD"),
            "aqs_email": os.environ.get("API_EPA_AQS_EMAIL"),
            "aqs_key": os.environ.get("API_EPA_AQS"),
        })
        await self.execute(command)
        await super().setup(context_info, parent_header=parent_header)

    async def default_preamble(self):
        return f"""
*	Before generating any code, come up with a plan and run it by me. If after you start to write or execute code you find that a resource is not available or something won’t work well, create a new plan and run it by me before writing and executing more code.
*	If you don't have information about what options to pick, ask me questions to get this before generating. Check that you have all the necessary info first. Also, if you are unsure about an identifier or anything else, don't guess-- please ask me.
*	In your results summary, include a concise summary of your methods, include the resources you used, any logic and options you used, any selections you made, and any assumptions you made.
*	In your results summary, for every piece of information you report, include a footnote about the resource(s) you obtained the information from and indicate the code block and code lines that were responsible for generating this information. If it came from your general knowledge, please indicate that.
"""
