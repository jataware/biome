from typing import TYPE_CHECKING, Any, Dict, List
import os
import json
import re
import logging

from pathlib import Path

from beaker_kernel.lib.context import BaseContext, action
from beaker_kernel.subkernels.python import PythonSubkernel
from beaker_kernel.lib.types import Datasource, DatasourceAttachment

from .agent import DATASOURCES_FOLDER, BiomeAgent

if TYPE_CHECKING:
    from beaker_kernel.kernel import LLMKernel
    from beaker_kernel.lib.agent import BaseAgent

logger = logging.getLogger(__name__)


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
            "synapse_api_key": os.environ.get("API_SYNAPSE"),
            "netrias_api_key": os.environ.get("NETRIAS_KEY"),
        })
        await self.execute(command)

    async def get_datasources(self) -> list[Datasource]:
        """
        fetch all of the adhoc-api datasources to pass to beaker.
        """

        # get list of keys not inherent to a datasource for the user-files category
        attached_files = {}
        for (_, spec) in self.agent.raw_specs:
            attached_files[spec['name']] = []
            for attachment_key in [
                key for key in spec.keys() if key not in [
                    "name",
                    "slug",
                    "description",
                    "cache_key",
                    "documentation",
                    "examples",
                    "cache_body"
                ]
            ]:
                if not isinstance(spec[attachment_key], str):
                    logger.warning(f"warning: key {attachment_key} on spec {spec['name']} is of type {type(spec[attachment_key])} and not str. ignoring and continuing")
                    continue

                # trim yaml tags since they will be readded at save time
                # TODO: handle not-eliding documentation/
                filepath_raw = re.sub(
                        r'!load_[a-zA-Z]+',
                        '',
                        spec[attachment_key].strip()
                    ).strip().replace('documentation/', '')

                attached_files[spec['name']].append(DatasourceAttachment(
                    name=attachment_key,
                    filepath=filepath_raw,
                    content=None,
                    is_empty_file=False
                ))

        return [
            Datasource(
                slug=spec['slug'],
                url=str(yaml_location),
                name=spec['name'],
                description=spec.get('description'),
                source=spec.get('documentation').replace('!fill', ''),
                attached_files=attached_files[spec['name']]
            )
            for (yaml_location, spec) in self.agent.raw_specs
        ]

    @action(action_name="save_datasource")
    async def save_datasource(self, message):
        content = message.content

        datasource = Datasource(
            name=content.get('name'),
            slug=content.get('slug'),
            url=content.get('url'),
            description=content.get('description'),
            source=content.get('source'),
            attached_files=[
                DatasourceAttachment(
                    name=payload['name'],
                    filepath=payload['filepath']
                )
                for payload in content.get('attached_files')]
        )

        slug = datasource.slug
        indented_contents = ''.join(
            [f"\n    {line}" for line in (datasource.source or "").splitlines()]
        )
        indented_description = ''.join(
            [f"\n    {line}" for line in (datasource.description or "").splitlines()]
        )

        attached_files = [
            f"{attachment.name}: !load_txt documentation/{attachment.filepath}\n"
            for attachment in datasource.attached_files or []
        ]
        file_payload = '\n'.join(attached_files)

        api_yaml = f"""
name: {datasource.name}
slug: {slug}
cache_key: api_assistant_{slug}
examples: !load_yaml documentation/examples.yaml

description: |
    {indented_description.strip()}

{file_payload}

documentation: !fill |
    {indented_contents.strip()}
"""
        url = datasource.url
        if url is None or url == "":
            url = Path(slug) / 'api.yaml'
        full_path = Path(self.agent.root_folder) / DATASOURCES_FOLDER / url
        os.makedirs(str(full_path)[0:-9], exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(api_yaml)

        examples_path = f"{str(full_path)[0:-9]}/documentation/examples.yaml"
        if not os.path.isfile(examples_path):
            with open(examples_path, 'a') as f:
                f.write('')
        self.agent.fetch_specs()
        self.agent.initialize_adhoc()
