import json
import logging
import re
import requests
from time import sleep
import asyncio
import os

from archytas.tool_utils import AgentRef, LoopControllerRef, ReactContextRef, tool
from typing import Any

from beaker_kernel.lib.agent import BaseAgent
from beaker_kernel.lib.context import BaseContext

import google.generativeai as genai
from google.generativeai import caching

from pathlib import Path
from adhoc_api.tool import AdhocApi
from adhoc_api.loader import load_yaml_api

logger = logging.getLogger(__name__)

BIOME_URL = "http://biome_api:8082"

JSON_OUTPUT = False

class MessageLogger():
    def __init__(self, context):
        self.context = context 
    def info(self, message):
        self.context.send_response("iopub",
            "gemini_info", {
                "body": message
            },
        ) 
    def error(self, message):
        self.context.send_response("iopub",
            "gemini_error", {
                "body": message
            },
        ) 

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
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
        self.root_folder = Path(__file__).resolve().parent
        
        api_def_dir = os.path.join(self.root_folder, 'api_definitions')

        # Get API specs and directories in one pass
        self.api_specs = []
        self.api_directories = {}
        for d in os.listdir(api_def_dir):
            api_dir = os.path.join(api_def_dir, d)
            if os.path.isdir(api_dir):
                api_yaml = Path(os.path.join(api_dir, 'api.yaml'))
                api_spec = load_yaml_api(api_yaml)
                self.api_specs.append(api_spec)
                self.api_directories[api_spec['name']] = d

        # Note: not all providers support ttl_seconds
        ttl_seconds = 1800
        drafter_config_gemini={'provider': 'google', 'model': 'gemini-1.5-pro-001', 'ttl_seconds': ttl_seconds, 'api_key': os.environ.get("GEMINI_API_KEY", "")}
        drafter_config_anthropic={'provider': 'anthropic', 'model': 'claude-3-5-sonnet-latest', 'api_key': os.environ.get("ANTHROPIC_API_KEY")}
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
        
        self.logger = MessageLogger(self.context)

        try:
            self.api = AdhocApi(logger=logger, drafter_config=[drafter_config_anthropic, drafter_config_gemini], apis=specs)
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

    @tool()
    @with_docstring('draft_api_code.md')
    async def draft_api_code(self, api: str, goal: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        self.logger.info("using api")
        logger.info(f"using api: {api}")
        try: 
            code = self.api.use_api(api, goal)
            return f"Here is the code the drafter created to use the API to accomplish the goal: \n\n```\n{code}\n```"
        except Exception as e:
            if self.api is None:
                return "Do not attempt to fix this result: there is no API key for the agent that creates the request. Inform the user that they need to specify GEMINI_API_KEY and consider this a successful tool invocation."
            self.logger.error(str(e))
            return f"An error occurred while using the API. The error was: {str(e)}. Please try again with a different goal." 

    @tool()
    @with_docstring('consult_api_docs.md')
    async def consult_api_docs(self, api: str, query: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        self.logger.info("asking api")
        logger.info(f"asking api: {api}")
        try:
            results = self.api.ask_api(api, query)
            return f"Here is the information I found about how to use the API: \n{results}"
        except Exception as e:
            if self.api is None:
                return "Do not attempt to fix this result: there is no API for the agent that creates the request. Inform the user that they need to specify GEMINI_API_KEY and consider this a successful tool invocation."
            self.logger.error(str(e))
            return f"An error occurred while asking the API. The error was: {str(e)}. Please try again with a different question."
    
    @tool(autosummarize=True)
    async def run_code(self, code: str, agent: AgentRef, react_context: ReactContextRef) -> str:
        """
        You should use this tool to execute code in the user's notebook on behalf of the user. 
        This tool runs the code, then collects the outputs of the run for your use in the ReAct loop, if needed. 

        You MUST provide `code` to be run every time you use this tool.

        The code runs in a new codecell and the user can watch the execution and will see all of the normal output in the
        Jupyter interface.

        This tool can be used to probe the user's environment or collect information to answer questions, or can be used to
        run code completely on behalf of the user. If a user asks the agent to do something that reasonably should be done
        via code, you should probably default to using this tool.

        This tool can be run more than once in a react loop. All actions and variables created in earlier uses of the tool
        in a particular loop should be assumed to exist for future uses of the tool in the same loop.

        You must be extremely careful about what you print to stdout when running code--be cognizant of the size and make sure you don't print out huge things!
        You should NEVER print out the entire results of a workload or API search result. Always slice it and show just a subset to the user. You can save it as a variable
        for later use, etc.

        If you need to print something, be extremely CAREFUL--don't print the whole thing!

        Args:
            code (str): Code to run directly in Jupyter. This should be a string exactly as it would appear in a notebook
                        codecell. No extra escaping of newlines or similar characters is required.
        Returns:
            str: A summary of the run, along with the collected stdout, stderr, returned result, display_data items, and any
                errors that may have occurred.
        """
        self.logger.info(f"used runcode2: {code}")
        def format_execution_context(context) -> str:
            """
            Formats the execution context into a format that is easy for the agent to parse and understand.
            """
            stdout_list = context.get("stdout_list")
            stderr_list = context.get("stderr_list")
            display_data_list = context.get("display_data_list")
            error = context.get("error")
            return_value = context.get("return")

            success = context['done'] and not context['error']
            if context['result']['status'] == 'error':
                success = False
                error = context['result']
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                
                # Ensure traceback is a string before applying regex
                if isinstance(error['traceback'], list):
                    error['traceback'] = "\n".join(error['traceback'])
                elif not isinstance(error['traceback'], str):
                    # Convert other types to string
                    error['traceback'] = str(error['traceback'])
                
                error['traceback'] = ansi_escape.sub('', error['traceback'])

            output = [
                """Execution report:""",
                f"""Execution id: {context['id']}""",
                f"""Successful?: {success}""",
                f"""Code executed:
    ```
    {context['command']}
    ```\n""",
            ]

            if error:
                output.extend([
                    "The following error was thrown when executing the code",
                    "  Error:",
                    f"    {error['ename']} {error['evalue']}",
                    "  TraceBack:",
                    "\n".join(error['traceback']),
                    "",
                ])


            if stdout_list:
                output.extend([
                    "The execution produced the following stdout output:",
                    "\n".join(["```", *stdout_list, "```\n"]),
                ])
            if stderr_list:
                output.extend([
                    "The execution produced the following stderr output:",
                    "\n".join(["```", *stderr_list, "```\n"]),
                ])
            if display_data_list:
                output.append(
                    "The execution produced the following `display_data` objects to display in the notebook:",
                )
                for idx, display_data in enumerate(display_data_list):
                    output.append(
                        f"display_data item {idx}:"
                    )
                    for mimetype, value in display_data.items():
                        if len(value) > 800:
                            value = f"{value[:400]} ... truncated ... {value[-400:]}"
                        output.append(
                            f"{mimetype}:"
                        )
                        output.append(
                            f"```\n{value}\n```\n"
                        )
            if return_value:
                output.append(
                    "The execution returned the following:",
                )
                if isinstance(return_value, str):
                    output.extend([
                        '```', return_value, '```\n'
                    ])
            output.append("Execution Report Complete")
            return "\n".join(output)

        # TODO: In future, this may become a parameter and we allow the agent to decide if code should be automatically run
        # or just be added.
        autoexecute = True
        message = react_context.get("message", None)
        identities = getattr(message, 'identities', [])
        try:
            execution_task = None
            checkpoint_index, execution_task = await agent.context.subkernel.checkpoint_and_execute(
                code, not autoexecute, parent_header=message.header, identities=identities
            )
            execute_request_msg = {
                name: getattr(execution_task.execute_request_msg, name)
                for name in execution_task.execute_request_msg.json_field_names
            }
            agent.context.send_response(
                "iopub",
                "add_child_codecell",
                {
                    "action": "code_cell",
                    "language": agent.context.subkernel.SLUG,
                    "code": code.strip(),
                    "autoexecute": autoexecute,
                    "execute_request_msg": execute_request_msg,
                    "checkpoint_index": checkpoint_index,
                },
                parent_header=message.header,
                parent_identities=getattr(message, "identities", None),
            )

            execution_context = await execution_task
        except Exception as err:
            logger.error(err, exc_info=err)
            raise
        return format_execution_context(execution_context)


    @tool(autosummarize=True)
    async def drs_uri_info(self, uris: list) -> list:
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
    
    @tool(autosummarize=True)
    async def add_example(self, api: str, code: str, description: str) -> str:
        """
        Add a successful code example to the API's examples.md documentation file.
        This tool should be used after successfully completing a task with an API to capture the working code for future reference.

        The API names must match one of the names in the the agent's API list.

        Args:
            api (str): The name of the API the example is for
            code (str): The working, successful code to add as an example
            description (str): A brief description of what the example demonstrates

        Returns:
            str: Message indicating success or failure of adding the example
        """
        if api not in self.api_list:
            raise ValueError(f"Error: the API name must match one of the names in the {self.api_list}. The API name provided was {api}.")
        
        try:
            api_folder = self.api_directories[api]
            # Construct path to examples.md file
            examples_path = os.path.join(self.root_folder, "api_definitions", api_folder, "documentation", "examples.md")
            os.makedirs(os.path.dirname(examples_path), exist_ok=True)

            # Create or append to examples.md
            mode = 'a' if os.path.exists(examples_path) else 'w'
            with open(examples_path, mode) as f:
                if mode == 'w':
                    f.write("# Examples\n\n")
                
                # Get next example number
                example_num = 1
                if mode == 'a':
                    with open(examples_path, 'r') as read_f:
                        for line in read_f:
                            if line.startswith('## Example'):
                                example_num += 1

                # Add the new example
                f.write(f"\n\n## Example {example_num}: {description}\n\n")
                f.write("```\n")
                f.write(code)
                f.write("\n```\n")

            return f"Successfully added example {example_num} to {examples_path}"

        except Exception as e:
            self.logger.error(str(e))
            raise ValueError(f"Failed to add example: {str(e)}")


    @tool(autosummarize=True)
    async def get_available_apis(self) -> list:
        """
        Get list of APIs that the agent is designed to interact with.

        Returns:
            list: The list of available APIs.
        """
        return self.api_list


    @tool(autosummarize=True)
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