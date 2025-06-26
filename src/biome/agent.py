import logging
import requests
import os

from archytas.tool_utils import AgentRef, LoopControllerRef, ReactContextRef, tool
from typing import List

from beaker_kernel.lib.agent import BeakerAgent
from beaker_kernel.lib.context import BaseContext

from pathlib import Path

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
def load_docstring(filename):
    root_folder = Path(__file__).resolve().parent / 'adhoc_data'
    with open(os.path.join(root_folder, 'prompts', filename), 'r') as f:
        return f.read()

def with_docstring(filename):
    """Decorator to set a function's docstring from a file"""
    docstring = load_docstring(filename)
    def decorator(func):
        func.__doc__ = docstring
        return func
    return decorator

class BiomeAgent(BeakerAgent):
    """
    You are the Biome Agent, a chat assistant that helps users with biomedical research tasks.

    An 'integration' is defined as an API or dataset or general collection of knowledge that you have access to.

    An API should be considered a type of integration.
    """
    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
        self.logger = MessageLogger(self.log, logger)
        super().__init__(context, tools, **kwargs)

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

    # @tool()
    # async def add_example(self, integration: str, code: str, query: str, notes: str = None) -> str:
    #     """
    #     Add a successful code example to the integration's examples.yaml documentation file.
    #     This tool should be used after successfully completing a task with an integration to capture the working code for future reference.

    #     The API names must match one of the names in the agent's integration list.

    #     Args:
    #         integration (str): The name of the integration the example is for
    #         code (str): The working, successful code to add as an example
    #         query (str): A brief description of what the example demonstrates
    #         notes (str, optional): Additional notes about the example, such as implementation details

    #     Returns:
    #         str: Message indicating success or failure of adding the example
    #     """
    #     if integration not in self.integration_list:
    #         raise ValueError(f"Error: the API name must match one of the names in the {self.integration_list}. The API name provided was {api}.")

    #     self.context.beaker_kernel.send_response(
    #         "iopub", "add_example", content={
    #             "integration": integration,
    #             "code": code,
    #             "query": query,
    #             "notes": notes
    #         }
    #     )
    #     return "Successfully added example."

    # @tool()
    # async def add_integration(self,
    #                          integration: str,
    #                          description: str,
    #                          base_url: str,
    #                          schema_location: str) -> str:
    #     """
    #     Adds an integration to the list of supported integrations usable within Biome.
    #     This will be added to the API and data source list.

    #     Args:
    #         integration (str): The name of the target data source or API that will be added.
    #         description (str): A plain text description of what the data source is based on your knowledge of what the user is asking for, combined with their description if their description is relevant, or, if you do not know about the target data source. If the user does not provide any information, rely on what you know. Target a paragraph in length.
    #         schema_location (str): A URL or local filepath to fetch an OpenAPI schema from. If the user does not provide one, ask them for the URL or local filepath to the schema.
    #         base_url (str): The base URL for the integration that will be used for making OpenAPI calls. If the user does not provide one, ask them for the base URL of the API.
    #     Returns:
    #         str: Message indicating success or failure of adding the integration.
    #     """

    #     try:
    #         if schema_location.startswith('http'):
    #             response = requests.get(schema_location)
    #             if response.status_code != 200:
    #                 return f'Failed to get OpenAPI schema: {response.status_code}'
    #             schema = response.content.decode("utf-8")
    #         else:
    #             with open(schema_location, 'r') as f:
    #                 schema = f.read()
    #     except Exception as e:
    #         return f'Failed to get OpenAPI schema: {e}'

    #     # calls save_integration in context.py as an action after finishing
    #     self.context.beaker_kernel.send_response(
    #         "iopub", "add_integration", content={
    #             "integration": integration,
    #             "description": description,
    #             "base_url": base_url,
    #             "schema": schema
    #         }
    #     )
    #     return f"Added integration `{integration}`."

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
