import json
import logging
import re
import requests
from time import sleep
import asyncio
import os

from archytas.tool_utils import AgentRef, LoopControllerRef, ReactContextRef, tool
from typing import Any, List

from beaker_kernel.lib.agent import BaseAgent
from beaker_kernel.lib.context import BaseContext
import yaml

from pathlib import Path
from adhoc_api.tool import AdhocApi, ensure_name_slug_compatibility
from adhoc_api.loader import load_yaml_api
from adhoc_api.uaii import gpt_4o, o3_mini, claude_37_sonnet, gemini_15_pro

logger = logging.getLogger(__name__)

BIOME_URL = "http://biome_api:8082"

JSON_OUTPUT = False

DATASOURCES_FOLDER = "datasources"

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
def load_docstring(filename):
    root_folder = Path(__file__).resolve().parent
    with open(os.path.join(root_folder, 'prompts', filename), 'r') as f:
        return f.read()

def with_docstring(filename):
    """Decorator to set a function's docstring from a file"""
    docstring = load_docstring(filename)
    def decorator(func):
        func.__doc__ = docstring
        return func
    return decorator

DRAFT_API_CODE_DOC = load_docstring('draft_api_code.md')
CONSULT_API_DOCS_DOC = load_docstring('consult_api_docs.md')

class BiomeAgent(BaseAgent):
    """
    You are the Biome Agent, a chat assistant that helps users with biomedical research tasks.

    A 'datasource' is defined as an API or dataset or general collection of knowledge that you have access to.

    An API should be considered a type of datasource.
    """
    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        self.root_folder = Path(__file__).resolve().parent

        self.fetch_specs()

        instructions_dir = os.path.join(self.root_folder, 'instructions')
        # join all the files in the instructions directory into a single string
        self.instructions = ""
        for file in os.listdir(instructions_dir):
            with open(os.path.join(instructions_dir, file), 'r') as f:
                self.instructions += f.read()

        super().__init__(context, tools, **kwargs)
        sleep(5)

        # Configure root logger
        logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))

        self.logger = MessageLogger(self.log, logger)

        self.initialize_adhoc()

        # Load prompt files and set the Agent context
        prompts_dir = os.path.join(self.root_folder, 'prompts')
        with open(os.path.join(prompts_dir, 'agent_prompt.md'), 'r') as f:
            template = f.read()
            self.__doc__ = template.format(api_list=self.api_list, instructions=self.instructions)
            self.add_context(self.__doc__)

    def fetch_specs(self):
        api_def_dir = os.path.join(self.root_folder, DATASOURCES_FOLDER)
        data_dir = (self.root_folder / ".." / "..").resolve() / "data"
        self.data_dir = data_dir
        print(f"data_dir: {data_dir}")

        # Get API specs and directories in one pass
        self.api_specs = []
        self.raw_specs = [] # no interpolation
        self.api_directories = {}
        for d in os.listdir(api_def_dir):
            if d == '.ipynb_checkpoints':
                os.rmdir(os.path.join(api_def_dir, d))
            api_dir = os.path.join(api_def_dir, d)
            if os.path.isdir(api_dir):
                api_yaml = Path(os.path.join(api_dir, 'api.yaml'))
                if not os.path.isfile(api_yaml):
                    logger.warning(f"Ignoring malformed API: {api_yaml}")
                    continue

                api_spec = load_yaml_api(api_yaml)
                # custom yaml loader to ignore tags to not pre-interpolate before editing
                with open(api_yaml, 'r') as f:
                    def ignore_tags(loader, tag_suffix, node):
                        return tag_suffix + ' ' + node.value
                    yaml.add_multi_constructor('', ignore_tags, yaml.SafeLoader)
                    raw_spec = yaml.safe_load(f)
                    try:
                        ensure_name_slug_compatibility(raw_spec)
                        self.raw_specs.append((os.path.join(d, 'api.yaml'), raw_spec))
                    except Exception as e:
                        logger.error(f"Failed to load datasource `{api_yaml}` from raw yaml: {e}")

                # Replace {DATASET_FILES_BASE_PATH} with data_dir path; { and {{ to reduce mental overhead
                api_spec['documentation'] = api_spec['documentation'].replace('{DATASET_FILES_BASE_PATH}', str(data_dir))
                api_spec['documentation'] = api_spec['documentation'].replace('{{DATASET_FILES_BASE_PATH}}', str(data_dir))

                if 'examples' in api_spec and isinstance(api_spec['examples'], list):
                    for example in api_spec['examples']:
                        if 'code' in example and isinstance(example['code'], str):
                            example['code'] = example['code'].replace('{{DATASET_FILES_BASE_PATH}}', str(data_dir))
                            example['code'] = example['code'].replace('{DATASET_FILES_BASE_PATH}', str(data_dir))

                ensure_name_slug_compatibility(api_spec)
                self.api_specs.append(api_spec)
                self.api_directories[api_spec['slug']] = d

    def initialize_adhoc(self):
        # Note: not all providers support ttl_seconds
        ttl_seconds = 1800
        drafter_config_gemini =    {**gemini_15_pro, 'ttl_seconds': ttl_seconds, 'api_key': os.environ.get("GEMINI_API_KEY", "")}
        drafter_config_anthropic = {**claude_37_sonnet, 'api_key': os.environ.get("ANTHROPIC_API_KEY")}
        curator_config =           {**o3_mini, 'api_key': os.environ.get("OPENAI_API_KEY")}
        contextualizer_config =    {**gpt_4o, 'api_key': os.environ.get("OPENAI_API_KEY")}
        specs = self.api_specs

        try:
            self.api = AdhocApi(
                apis=specs,
                drafter_config=[drafter_config_anthropic, drafter_config_gemini],
                curator_config=curator_config,
                contextualizer_config=contextualizer_config,
                logger=self.logger,
            )
        except ValueError as e:
            self.add_context(f"The datasources failed to load for this reason: {str(e)}. Please inform the user immediately.")
            self.api = None

        self.api_list = [spec['slug'] for spec in specs]

    def log(self, event_type: str, content = None) -> None:
        self.context.beaker_kernel.log(
            event_type=f"agent_{event_type}",
            content=content
        )

    @tool()
    @with_docstring('draft_api_code.md')
    async def draft_api_code(self, api: str, goal: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        logger.info(f"using api: {api}")
        try:
            code = self.api.use_api(api, goal)
            return f"Here is the code the drafter created to use the API to accomplish the goal: \n\n```\n{code}\n```"
        except Exception as e:
            if self.api is None:
                return "Do not attempt to fix this result: there is no API key for the agent that creates the request. Inform the user that they need to specify GEMINI_API_KEY and consider this a successful tool invocation."
            logger.error(str(e))
            return f"An error occurred while using the API. The error was: {str(e)}. Please try again with a different goal."

    @tool()
    @with_docstring('consult_api_docs.md')
    async def consult_api_docs(self, api: str, query: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        logger.info(f"asking api: {api}")
        try:
            results = self.api.ask_api(api, query)
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
    async def add_example(self, api: str, code: str, query: str, notes: str = None) -> str:
        """
        Add a successful code example to the datasource's examples.yaml documentation file.
        This tool should be used after successfully completing a task with an datasource to capture the working code for future reference.

        The API names must match one of the names in the agent's datasource list.

        Args:
            api (str): The name of the datasource the example is for
            code (str): The working, successful code to add as an example
            query (str): A brief description of what the example demonstrates
            notes (str, optional): Additional notes about the example, such as implementation details

        Returns:
            str: Message indicating success or failure of adding the example
        """
        if api not in self.api_list:
            raise ValueError(f"Error: the API name must match one of the names in the {self.api_list}. The API name provided was {api}.")
        
        try:
            api_folder = self.api_directories[api]
            # Construct path to examples.yaml file
            examples_path = os.path.join(self.root_folder, DATASOURCES_FOLDER, api_folder, "documentation", "examples.yaml")
            os.makedirs(os.path.dirname(examples_path), exist_ok=True)
            
            # Create new example entry as a dictionary
            new_example = {
                "query": query,
                "code": code  # Will be formatted with block scalar style
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
    async def add_datasource(self,
                             datasource: str,
                             description: str,
                             base_url: str,
                             schema_location: str) -> str:
        """
        Adds a datasource to the list of supported datasources usable within Biome.
        This will be added to the API and data source list.

        Args:
            datasource (str): The name of the target data source or API that will be added.
            description (str): A plain text description of what the data source is based on your knowledge of what the user is asking for, combined with their description if their description is relevant, or, if you do not know about the target data source. If the user does not provide any information, rely on what you know. Target a paragraph in length.
            schema_location (str): A URL or local filepath to fetch an OpenAPI schema from. If the user does not provide one, ask them for the URL or local filepath to the schema.
            base_url (str): The base URL for the datasource that will be used for making OpenAPI calls. If the user does not provide one, ask them for the base URL of the API.
        Returns:
            str: Message indicating success or failure of adding the datasource.
        """
        datasources_path = os.path.join(self.root_folder, DATASOURCES_FOLDER)
        datasource_name = datasource.lower().replace(' ', '_')
        datasource_folder = os.path.join(datasources_path, datasource_name)
        if (os.path.isdir(datasource_folder)):
            return f"Failed to add datasource: {datasource}: {DATASOURCES_FOLDER}/{datasource_folder} already exists."

        logger.info(f'adding datasource {datasource} to {datasource_folder}')
        try:
            if schema_location.startswith('http'):
                response = requests.get(schema_location)
                if response.status_code != 200:
                    return f'Failed to get OpenAPI schema: {response.status_code}'
                schema = response.content.decode("utf-8")
            else:
                with open(schema_location, 'r') as f:
                    schema = f.read()

            documentation_folder = os.path.join(datasource_folder, 'documentation')
            os.makedirs(documentation_folder, exist_ok=True)
            with open(os.path.join(documentation_folder, 'schema.yaml'), 'w') as f:
                f.write(str(schema))
            with open(os.path.join(documentation_folder, 'examples.yaml'), 'a'):
                pass

        except Exception as e:
            return f'Failed to get OpenAPI schema: {e}'

        formatted_description = description.replace('\n', ' ')
        template = f"""
name: {datasource}
description: {formatted_description}
examples: !load_yaml documentation/examples.yaml
cache_key: "api_assistant_{datasource_name}"
raw_documentation: !load_txt documentation/schema.yaml

documentation: !fill |
    The base URL for the service is `{base_url}`
    Below is the OpenAPI schema for the desired service.

    {{raw_documentation}}
"""
        with open(os.path.join(datasource_folder, 'api.yaml'), 'w') as f:
            f.write(template)
        try:
            datasource_yaml = Path(os.path.join(datasource_folder, 'api.yaml'))
            datasource_spec = load_yaml_api(datasource_yaml)
            self.api_specs.append(datasource_spec)
            self.api.add_api(datasource_spec)

        except Exception as e:
            return f"Failed to add datasource: {e}"
        logger.info(f'Successfully added {datasource} to {datasource_folder} and it is now available for use.')
        return f'Successfully added {datasource} and it is now available for use.'

    @tool()
    async def get_available_datasources(self) -> list:
        """
        Get list of datasources that the agent is designed to interact with.

        Returns:
            list: The list of available datasources.
        """
        return self.api_list


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
