from typing import TYPE_CHECKING, Any, Dict
import os
import re
import logging
import json

from jupyter_server.services.contents.filemanager import (
    FileContentsManager,
)

from pathlib import Path

from beaker_kernel.lib.context import BeakerContext, action
from beaker_kernel.subkernels.python import PythonSubkernel
from beaker_kernel.lib.types import Integration, IntegrationAttachment

from .agent import BiomeAgent
from .integration import create_folder_structure_for_integration, get_integration_folder, write_integration

if TYPE_CHECKING:
    from beaker_kernel.kernel import LLMKernel
    from beaker_kernel.lib.agent import BaseAgent


logger = logging.getLogger(__name__)


class BiomeContext(BeakerContext):

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
            "synapse_api_key": os.environ.get("API_SYNAPSE"),
            "netrias_api_key": os.environ.get("NETRIAS_KEY"),
        })
        await self.execute(command)

    async def get_integrations(self) -> list[Integration]:
        """
        fetch all of the adhoc-api integrations to pass to beaker.
        """

        # get list of keys not inherent to a integrations for the user-files category
        attached_files = {}
        for (_, spec) in self.agent.raw_specs:
            attached_files[spec["name"]] = []
            for attachment_key in [
                key for key in spec.keys() if key not in [
                    "name",
                    "slug",
                    "description",
                    "cache_key",
                    "documentation",
                    "examples",
                    "cache_body",
                    "loaded_examples"
                ]
            ]:
                if not isinstance(spec[attachment_key], str):
                    logger.warning(f"warning: key {attachment_key} on spec {spec['name']} is of type {type(spec[attachment_key])} and not str. ignoring and continuing")
                    continue

                # trim yaml tags since they will be readded at save time
                # TODO: handle not-eliding documentation/
                filepath_raw = re.sub(
                        r"!load_[a-zA-Z]+",
                        "",
                        spec[attachment_key].strip()
                    ).strip().replace("documentation/", "")

                attached_files[spec["name"]].append(IntegrationAttachment(
                    name=attachment_key,
                    filepath=filepath_raw,
                    content=None,
                    is_empty_file=False
                ))

        # manually load examples

        return [
            Integration(
                slug=spec["slug"],
                url=str(yaml_location),
                name=spec["name"],
                description=spec.get("description"),
                source=spec.get("documentation").replace("!fill", ""),
                attached_files=attached_files[spec["name"]],
                examples=spec.get("loaded_examples", [])
            )
            for (yaml_location, spec) in self.agent.raw_specs
        ]

    async def save_integration(self, message):
        logger.warning('called save_integration')
        manager = FileContentsManager()
        content = message.content
        write_integration(manager, content)
        self.agent.fetch_specs()
        self.agent.initialize_adhoc()
        self.agent.add_context(f"A new integration has been added: `{content.get('slug')}`. You may now use this with `draft_integration_code`.")

    async def add_example(self, message):
        logger.warning('called add_example')
        manager = FileContentsManager()
        content = message.content
        logger.warning(content)
        write_integration(manager, content)
        self.agent.fetch_specs()
        self.agent.initialize_adhoc()
        self.agent.add_context(f"A new example has been added to `{content.get('slug')}.`")
