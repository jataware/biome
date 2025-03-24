from typing import TYPE_CHECKING, Any, Dict, List
import os

from beaker_kernel.lib.context import BaseContext
from beaker_kernel.lib.subkernels.python import PythonSubkernel

from .agent import BiomeAgent

if TYPE_CHECKING:
    from beaker_kernel.kernel import LLMKernel
    from beaker_kernel.lib.agent import BaseAgent

class BiomeContext(BaseContext):

    SLUG = "biome"
    agent_cls: "BaseAgent" = BiomeAgent

    def __init__(self, beaker_kernel: "LLMKernel", config: Dict[str, Any]):
        super().__init__(beaker_kernel, self.agent_cls, config)
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
        })
        await self.execute(command)