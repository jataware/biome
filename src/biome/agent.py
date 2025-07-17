import json
import logging
import re
import requests
from time import sleep
import asyncio
import os

from archytas.tool_utils import AgentRef, LoopControllerRef, ReactContextRef, tool
from typing import Any, List

from beaker_kernel.lib.agent import BeakerAgent
from beaker_kernel.lib.context import BaseContext
import yaml

from pathlib import Path
from adhoc_api.tool import AdhocApi, ensure_name_slug_compatibility
from adhoc_api.loader import load_yaml_api
from adhoc_api.uaii import gpt_41, o3_mini, claude_37_sonnet, gemini_15_pro

from Bio import Entrez

from biome.literature_review import LiteratureReviewAgent, PubmedSource

logger = logging.getLogger(__name__)

BIOME_URL = "http://biome_api:8082"

JSON_OUTPUT = False

INTEGRATIONS_FOLDER = "datasources"

class MessageLogger():
    def __init__(self, agent_log_function, print_logger):
        self.agent_log = agent_log_function
        self.print_logger = print_logger
    def info(self, message):
        self.agent_log("Drafting Agent", message)
    def error(self, message):
        self.print_logger.error(message)
    def debug(self, message):
        self.print_logger.debug(message)

# Load docstrings at module level
def load_docstring(filename: str):
    root_folder = Path(__file__).resolve().parent
    return (root_folder / 'prompts' / 'docstrings' / filename).read_text()

def with_docstring(filename):
    """Decorator to set a function's docstring from a file"""
    docstring = load_docstring(filename)
    def decorator(func):
        func.__doc__ = docstring
        return func
    return decorator

# yaml loader that ignores !tag directives for getting raw yaml text from datasources
def ignore_tags(loader, tag_suffix, node):
    return tag_suffix + ' ' + node.value
yaml.add_multi_constructor('', ignore_tags, yaml.SafeLoader)

class BiomeAgent(BeakerAgent):
    """
    You are the Biome Agent, a chat assistant that helps users with biomedical research tasks.

    An 'integration' is defined as an API or dataset or general collection of knowledge that you have access to.

    An API should be considered a type of integration.
    """
    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        data_dir_raw = os.environ.get("BIOME_DATA_DIR", "./data")
        try:
            data_dir = Path(data_dir_raw).resolve(strict=True)
            logger.info(f"Using data_dir: {data_dir}")
        except OSError as e:
            data_dir = Path('.')
            logger.error(f"Failed to set biome data dir: {data_dir_raw} does not exist: {e}")
        self.data_dir = data_dir

        self.initialize_literature_review()
        self.initialize_entrez()

        logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
        self.logger = MessageLogger(self.log, logger)

        self.root_folder = Path(__file__).resolve().parent
        self.fetch_specs()

        super().__init__(context, tools, **kwargs)
        self.initialize_adhoc()

        prompts_dir = self.root_folder / "prompts"
        extra_agent_prompts_dir = prompts_dir / "agent"
        main_agent_prompt = prompts_dir / "agent_prompt.md"

        self.extra_agent_prompts = "\n".join(
            file.read_text()
            for file in extra_agent_prompts_dir.iterdir() if file.is_file()
        )

        self.__doc__ = main_agent_prompt.read_text().format(
            api_list=self.integration_list,
            extra_prompts=self.extra_agent_prompts
        )
        self.add_context(self.__doc__)

    def initialize_literature_review(self):
        self.litreview_agent = LiteratureReviewAgent(self.data_dir)
        self.litreview_agent.add_source("pubmed", PubmedSource())

    def initialize_entrez(self):
        if (entrez_email := os.environ.get("ENTREZ_EMAIL", None)):
            Entrez.email = entrez_email
        if (entrez_key := os.environ.get("ENTREZ_API_KEY", None)):
            Entrez.api_key = entrez_key


    def fetch_specs(self):
        integration_root = os.path.join(self.root_folder, INTEGRATIONS_FOLDER)

        data_dir_raw = os.environ.get("BIOME_DATA_DIR", "./data")
        try:
            data_dir = Path(data_dir_raw).resolve(strict=True)
            logger.info(f"Using data_dir: {data_dir}")
        except OSError as e:
            data_dir = ''
            logger.error(f"Failed to set biome data dir: {data_dir_raw} does not exist: {e}")
        self.data_dir = data_dir

        # Get API specs and directories in one pass
        self.integration_specs = []
        self.raw_specs = [] # no interpolation
        self.integration_directories = {}
        for integration_dir in os.listdir(integration_root):
            if integration_dir == '.ipynb_checkpoints':
                try:
                    os.rmdir(os.path.join(integration_root, integration_dir))
                except IOError:
                    continue

            integration_full_path = os.path.join(integration_root, integration_dir)
            if os.path.isdir(integration_full_path):
                integration_yaml = Path(os.path.join(integration_full_path, 'api.yaml'))
                if not integration_yaml.is_file():
                    logger.warning(f"Ignoring malformed API: {integration_yaml}")
                    continue

                api_spec = load_yaml_api(integration_yaml)
                raw_contents = integration_yaml.read_text()
                raw_spec = yaml.safe_load(raw_contents)

                # Replace {DATASET_FILES_BASE_PATH} with data_dir path; { and {{ to reduce mental overhead
                api_spec['documentation'] = api_spec['documentation'].replace('{DATASET_FILES_BASE_PATH}', str(data_dir))
                api_spec['documentation'] = api_spec['documentation'].replace('{{DATASET_FILES_BASE_PATH}}', str(data_dir))

                if 'examples' in api_spec and isinstance(api_spec['examples'], list):
                    for example in api_spec['examples']:
                        if 'code' in example and isinstance(example['code'], str):
                            example['code'] = example['code'].replace('{{DATASET_FILES_BASE_PATH}}', str(data_dir))
                            example['code'] = example['code'].replace('{DATASET_FILES_BASE_PATH}', str(data_dir))

                try:
                    ensure_name_slug_compatibility(raw_spec)
                    # add the loaded examples in too, since we want that tag parsed but also the raw text as well
                    raw_spec['loaded_examples'] = api_spec.get('examples', [])
                    self.raw_specs.append((os.path.join(integration_dir, 'api.yaml'), raw_spec))
                except Exception as e:
                    logger.error(f"Failed to load integration `{integration_yaml}` from raw yaml: {e}")

                ensure_name_slug_compatibility(api_spec)
                self.integration_specs.append(api_spec)
                self.integration_directories[api_spec['slug']] = integration_dir

    def initialize_adhoc(self):
        # Note: not all providers support ttl_seconds
        ttl_seconds = 1800
        drafter_config_gemini =    {**gemini_15_pro, 'ttl_seconds': ttl_seconds, 'api_key': os.environ.get("GEMINI_API_KEY", "")}
        drafter_config_anthropic = {**claude_37_sonnet, 'api_key': os.environ.get("ANTHROPIC_API_KEY")}
        curator_config =           {**o3_mini, 'api_key': os.environ.get("OPENAI_API_KEY")}
        gpt_41_config =            {**gpt_41, 'api_key': os.environ.get("OPENAI_API_KEY")}
        specs = self.integration_specs

        try:
            self.api = AdhocApi(
                apis=specs,
                drafter_config=[gpt_41_config, drafter_config_anthropic, drafter_config_gemini],
                curator_config=curator_config,
                contextualizer_config=gpt_41_config,
                logger=self.logger,
            )
        except ValueError as e:
            self.add_context(f"The datasources failed to load for this reason: {str(e)}. Please inform the user immediately.")
            self.api = None

        self.integration_list = [spec['slug'] for spec in specs]

    def log(self, event_type: str, content = None) -> None:
        self.context.beaker_kernel.log(
            event_type=f"agent_{event_type}",
            content=content
        )

    @tool()
    @with_docstring('draft_integration_code.md')
    async def draft_integration_code(self, integration: str, goal: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        try:
            code = self.api.use_api(integration, goal)
            return f"Here is the code the drafter created to use the API to accomplish the goal: \n\n```\n{code}\n```"
        except Exception as e:
            if self.api is None:
                return "Do not attempt to fix this result: there is no API key for the agent that creates the request. Inform the user that they need to specify GEMINI_API_KEY and consider this a successful tool invocation."
            logger.error(str(e))
            return f"An error occurred while using the API. The error was: {str(e)}. Please try again with a different goal."

    @tool()
    @with_docstring('consult_integration_docs.md')
    async def consult_integration_docs(self, integration: str, query: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        try:
            results = self.api.ask_api(integration, query)
            return f"Here is the information I found about how to use the API: \n{results}"
        except Exception as e:
            if self.api is None:
                return "Do not attempt to fix this result: there is no API for the agent that creates the request. Inform the user that they need to specify GEMINI_API_KEY and consider this a successful tool invocation."
            logger.error(str(e))
            return f"An error occurred while asking the API. The error was: {str(e)}. Please try again with a different question."


    @tool()
    async def drs_uri_info(self, uris: List[str]) -> List[dict]:
        """
        Get information about a DRS URI.
        Data Repository Service (DRS) URIs are used to provide a standard way to locate and access data objects in a cloud environment.
        In the context of the Cancer Data Aggregator (CDA) API, DRS URIs are used to specify how to access data.

        Args:
            uris (list): A list of DRS URIs to get information about. URIs should be of the form 'drs://<hostname>:<id_number>'.

        Returns:
            list: The information from looking up each DRS URI.
        """
        responses = []
        for uri in uris:

            # Split the DRS URI by ':' and take the last part as the object ID
            if not uri.startswith("drs://"):
                raise ValueError("Invalid DRS URI: Must start with 'drs://'")
            try:
                object_id = uri.split(":")[-1]
            except IndexError:
                raise ValueError("Invalid DRS URI: Missing object ID")

            # Get information about the object from the DRS server
            url = f"https://nci-crdc.datacommons.io/ga4gh/drs/v1/objects/{object_id}"
            response = requests.get(url)
            response.raise_for_status()

            # Append the response to the list of responses
            responses.append(response.json())

        return responses

    @tool()
    async def add_example(self, integration: str, code: str, query: str, notes: str = None) -> str:
        """
        Add a successful code example to the integration's examples.yaml documentation file.
        This tool should be used after successfully completing a task with an integration to capture the working code for future reference.

        The API names must match one of the names in the agent's integration list.

        Args:
            integration (str): The name of the integration the example is for
            code (str): The working, successful code to add as an example
            query (str): A brief description of what the example demonstrates
            notes (str, optional): Additional notes about the example, such as implementation details

        Returns:
            str: Message indicating success or failure of adding the example
        """
        try:
            api_folder = self.api_directories[api]
            # Construct path to examples.yaml file
            examples_path = os.path.join(self.root_folder, DATASOURCES_FOLDER, api_folder, "documentation", "examples.yaml")
            os.makedirs(os.path.dirname(examples_path), exist_ok=True)

            # Create new example entry as a dictionary
            new_example = {
                "query": query,
                "notes": notes
            }

            # Add notes if provided
            if notes:
                new_example["notes"] = notes

            # Read existing examples if file exists
            examples = []
            if os.path.exists(examples_path) and os.path.getsize(examples_path) > 0:
                import yaml
                with open(examples_path, 'r') as f:
                    examples = yaml.safe_load(f) or []
                    if not isinstance(examples, list):
                        examples = []

            # Add new example
            examples.append(new_example)

            # Write updated examples back to file
            import yaml

            # Custom YAML dumper class that always uses block style for multiline strings
            class BlockStyleDumper(yaml.SafeDumper):
                pass

            # Always use block style (|) for strings with newlines
            def represent_str_as_block(dumper, data):
                if '\n' in data:
                    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
                return dumper.represent_scalar('tag:yaml.org,2002:str', data)

            BlockStyleDumper.add_representer(str, represent_str_as_block)

            with open(examples_path, 'w') as f:
                yaml.dump(examples, f, Dumper=BlockStyleDumper, sort_keys=False, default_flow_style=False)

            return f"Successfully added example to {examples_path}"

        except Exception as e:
            self.logger.error(str(e))
            raise ValueError(f"Failed to add example: {str(e)}")


    @tool()
    async def add_integration(self,
                             integration: str,
                             description: str,
                             base_url: str,
                             schema_location: str) -> str:
        """
        Adds an integration to the list of supported integrations usable within Biome.
        This will be added to the API and data source list.

        Args:
            integration (str): The name of the target data source or API that will be added.
            description (str): A plain text description of what the data source is based on your knowledge of what the user is asking for, combined with their description if their description is relevant, or, if you do not know about the target data source. If the user does not provide any information, rely on what you know. Target a paragraph in length.
            schema_location (str): A URL or local filepath to fetch an OpenAPI schema from. If the user does not provide one, ask them for the URL or local filepath to the schema.
            base_url (str): The base URL for the integration that will be used for making OpenAPI calls. If the user does not provide one, ask them for the base URL of the API.
        Returns:
            str: Message indicating success or failure of adding the integration.
        """

        try:
            if schema_location.startswith('http'):
                response = requests.get(schema_location)
                if response.status_code != 200:
                    return f'Failed to get OpenAPI schema: {response.status_code}'
                schema = response.content.decode("utf-8")
            else:
                with open(schema_location, 'r') as f:
                    schema = f.read()
        except Exception as e:
            return f'Failed to get OpenAPI schema: {e}'

        # calls save_integration in context.py as an action after finishing
        self.context.beaker_kernel.send_response(
            "iopub", "add_integration", content={
                "integration": integration,
                "description": description,
                "base_url": base_url,
                "schema": schema
            }
        )
        return f"Added integration `{integration}`."

    @tool()
    async def get_available_integrations(self) -> list:
        """
        Get list of integrations that the agent is designed to interact with.

        Returns:
            list: The list of available integrations.
        """
        return self.integration_list


    @tool()
    async def extract_pdf(self, pdf_path: str, agent: AgentRef) -> str:
        """
        Extract the text from a PDF file using PyPDF2. Note that if this tool
        fails for some reason you can fall back to using the `run_code` tool to
        extract the text using your own generated code.

        Args:
            pdf_path (str): The path to the PDF file to extract text from.

        Returns:
            str: The extracted text from the PDF file.
        """
        code = agent.context.get_code("extract_pdf", {'pdf_path': pdf_path})
        response = await agent.context.evaluate(code)
        return response["return"]


    @tool()
    async def pubmed_search(self, query: str):
        """
        Retrieves paper abstracts for a given PubMed query, as well as fetching the fulltexts for later.
        Relevant papers will be listed as their ID and associated abstracts.

        Try multiple formulations of the PubMed query to retrieve many papers.
        If less than five papers are found, retry this tool to see if other formulations find more papers.

        Args:
            query (str): User query to search on PubMed.

        Returns:
            str: Dictionary mapping the paper ID to the title and abstract and date, and full text PMC ID.
                 Additionally, search results will be available for paperQA.
        """
        return await self.litreview_agent.fetch_for_query("pubmed", query)


    @tool()
    async def paperQA(self, query: str, agent: AgentRef, loop: LoopControllerRef):
        """
        Given a corpus of fetched papers with `pubmed_search`, ask a question to analyze the
        collected papers and decide what's relevant and sort through the information.

        An example workflow would be grabbing all of the relevant papers with `pubmed_search` to find IDs,
        then get the full texts with `pubmed_get_fulltext` to gather them all -- and then finally, use this
        tool to get insights over all of the collected fulltext papers.

        You should return this full response, without any summarization, to the user.
        Important: do not summarize or shorten the response of this tool.

        CRITICAL: do not summarize or shorten the scientific explanation and output. Return it as-is.
        CRITICAL: DOI in every single citation. Cite where things were from in the PaperQA answer. Ensure the full title and doi are visible. Do not elide citations.

        Args:
            query (str): The query to ask about all of the papers

        Returns:
            str: CRITICAL: do not summarize or shorten the scientific explanation and output. Return it as-is. Include the DOI in every single citation. Cite where things were from in the PaperQA answer. Ensure the full title and doi are visible. Do not elide citations.
        """
        return await self.litreview_agent.paperQA(query)
