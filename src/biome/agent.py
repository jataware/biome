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

from pathlib import Path
from adhoc_api.tool import AdhocApi
from adhoc_api.loader import load_yaml_api
from adhoc_api.uaii import gpt_4o, o3_mini, claude_37_sonnet, gemini_15_pro

logger = logging.getLogger(__name__)

BIOME_URL = "http://biome_api:8082"

JSON_OUTPUT = False

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
    """

    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        self.root_folder = Path(__file__).resolve().parent

        api_def_dir = os.path.join(self.root_folder, 'api_definitions')
        data_dir = (self.root_folder / ".." / "..").resolve() / "data"
        print(f"data_dir: {data_dir}")

        # Get API specs and directories in one pass
        self.api_specs = []
        self.api_directories = {}
        for d in os.listdir(api_def_dir):
            api_dir = os.path.join(api_def_dir, d)
            if os.path.isdir(api_dir):
                api_yaml = Path(os.path.join(api_dir, 'api.yaml'))
                api_spec = load_yaml_api(api_yaml)

                # Replace {DATASET_FILES_BASE_PATH} with data_dir path; { and {{ to reduce mental overhead
                api_spec['documentation'] = api_spec['documentation'].replace('{DATASET_FILES_BASE_PATH}', str(data_dir))
                api_spec['documentation'] = api_spec['documentation'].replace('{{DATASET_FILES_BASE_PATH}}', str(data_dir))

                if 'examples' in api_spec and isinstance(api_spec['examples'], list):
                    for example in api_spec['examples']:
                        if 'code' in example and isinstance(example['code'], str):
                            example['code'] = example['code'].replace('{{DATASET_FILES_BASE_PATH}}', str(data_dir))
                            example['code'] = example['code'].replace('{DATASET_FILES_BASE_PATH}', str(data_dir))

                self.api_specs.append(api_spec)
                self.api_directories[api_spec['name']] = d

        # Note: not all providers support ttl_seconds
        ttl_seconds = 1800
        drafter_config_gemini =    {**gemini_15_pro, 'ttl_seconds': ttl_seconds, 'api_key': os.environ.get("GEMINI_API_KEY", "")}
        drafter_config_anthropic = {**claude_37_sonnet, 'api_key': os.environ.get("ANTHROPIC_API_KEY")}
        curator_config =           {**o3_mini, 'api_key': os.environ.get("OPENAI_API_KEY")}
        contextualizer_config =    {**gpt_4o, 'api_key': os.environ.get("OPENAI_API_KEY")}
        specs = self.api_specs

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

        try:
            self.api = AdhocApi(
                apis=specs,
                drafter_config=[drafter_config_anthropic, drafter_config_gemini],
                curator_config=curator_config,
                contextualizer_config=contextualizer_config,
                logger=self.logger,
            )
        except ValueError as e:
            self.add_context(f"The APIs failed to load for this reason: {str(e)}. Please inform the user immediately.")
            self.api = None

        self.api_list = [spec['name'] for spec in specs]

        # Load prompt files and set the Agent context
        prompts_dir = os.path.join(self.root_folder, 'prompts')
        with open(os.path.join(prompts_dir, 'agent_prompt.md'), 'r') as f:
            template = f.read()
            self.__doc__ = template.format(api_list=self.api_list, instructions=self.instructions)
            self.add_context(self.__doc__)

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
        Add a successful code example to the API's examples.yaml documentation file.
        This tool should be used after successfully completing a task with an API to capture the working code for future reference.

        The API names must match one of the names in the agent's API list.

        Args:
            api (str): The name of the API the example is for
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
            examples_path = os.path.join(self.root_folder, "api_definitions", api_folder, "documentation", "examples.yaml")
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
    async def get_available_apis(self) -> list:
        """
        Get list of APIs that the agent is designed to interact with.

        Returns:
            list: The list of available APIs.
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