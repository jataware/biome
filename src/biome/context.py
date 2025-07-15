from dataclasses import asdict
from typing import TYPE_CHECKING, Any, Dict
import os
import logging

from pathlib import Path

from beaker_kernel.lib.context import BeakerContext
from beaker_kernel.subkernels.python import PythonSubkernel
from beaker_kernel.lib.types import Integration
from beaker_kernel.lib.integrations.base import BaseIntegrationProvider
from beaker_kernel.lib.integrations.adhoc import AdhocIntegrationProvider

from .agent import BiomeAgent

if TYPE_CHECKING:
    from beaker_kernel.kernel import LLMKernel
    from beaker_kernel.lib.agent import BaseAgent


logger = logging.getLogger(__name__)

# TODO: Change this for better autodiscovery, etc
ADHOC_DIR_PATH = (Path(__file__).parent / "adhoc_data")


class TestIntegrationProvider(BaseIntegrationProvider):
    integrations: list[Integration]
    def __init__(self):
        self.integrations = [
            Integration(
                name="Test Integration 1",
                description="First Test Integration",
                provider="test"
            ),
            Integration(
                name="Test Integration 2",
                description="Second Test Integration",
                provider="test"
            ),
        ]
        super().__init__(display_name="Biome Second Test Integration")
    def list_integrations(self):
        return self.integrations
    def get_integration(self, integration_id):
        pass
    def list_resources(self, integration_id, resource_type=None):
        pass
    def get_resource(self, integration_id, resource_id):
        pass

class BiomeContext(BeakerContext):
    SLUG = "biome"
    agent_cls: "BaseAgent" = BiomeAgent

    def __init__(self, beaker_kernel: "LLMKernel", config: Dict[str, Any]):
        from adhoc_api.uaii import gpt_41, o3_mini, claude_37_sonnet, gemini_15_pro
        ttl_seconds = 1800
        drafter_config_gemini = {**gemini_15_pro, 'ttl_seconds': ttl_seconds, 'api_key': os.environ.get("GEMINI_API_KEY", "")}
        drafter_config_anthropic = {**claude_37_sonnet, 'api_key': os.environ.get("ANTHROPIC_API_KEY")}
        curator_config = {**o3_mini, 'api_key': os.environ.get("OPENAI_API_KEY")}
        gpt_41_config = {**gpt_41, 'api_key': os.environ.get("OPENAI_API_KEY")}

        # Initialize adhoc integration
        adhoc_integration = AdhocIntegrationProvider(
            adhoc_path=ADHOC_DIR_PATH,
            drafter_config=[gpt_41_config, drafter_config_anthropic, drafter_config_gemini],
            curator_config=curator_config,
            contextualizer_config=gpt_41_config,
            logger=logger,
            display_name="Specialist Agents"
        )
        test_integration = TestIntegrationProvider()
        super().__init__(
            beaker_kernel,
            self.agent_cls,
            config,
            integrations=[adhoc_integration, test_integration]
        )

        if not isinstance(self.subkernel, PythonSubkernel):
            raise ValueError("This context is only valid for Python.")

    async def setup(self, context_info=None, parent_header=None):
        """
        This runs on setup and invokes the `procedures/python3/setup.py` script to
        configure the environment appropriately.
        """
        command = self.get_code("setup", {
            "aqs_api_key": os.environ.get("API_EPA_AQS"),
            "aqs_email": os.environ.get("API_EPA_AQS_EMAIL"),
            "openfda_faers_api_key": os.environ.get("API_OPENFDA"),
            "usda_fdc_api_key": os.environ.get("API_USDA_FDC"),
            "census_api_key": os.environ.get("API_CENSUS"),
            "cdc_tracking_network_api_key": os.environ.get("API_CDC_TRACKING_NETWORK"),
            "synapse_api_key": os.environ.get("API_SYNAPSE"),
            "netrias_api_key": os.environ.get("NETRIAS_KEY"),
        })
        await self.execute(command)
