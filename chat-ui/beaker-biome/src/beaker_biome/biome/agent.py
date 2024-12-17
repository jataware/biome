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

import pathlib

from adhoc_api.tool import AdhocApi
from .yaml_loader import load, MessageLogger

logger = logging.getLogger(__name__)

BIOME_URL = "http://biome_api:8082"

JSON_OUTPUT = False

class BiomeAgent(BaseAgent):
    """
    You are a chat assistant that helps the analyst user with their questions. You are running inside of the Analyst UI which is a chat application
    sitting on top of a Jupyter notebook. This means the user will not be looking at code and will expect you to run code under the hood. Of course,
    power users may end up inspecting the code you you end up running and editing it.

    You have the ability to look up information regarding the environment via the tools that are provided. You should use these tools whenever are not able to
    satisfy the request to a high level of reliability. You should avoid guessing at how to do something in favor of using the provided tools to look up more
    information. Do not make assumptions, always check the documentation instead of assuming.

    You are currently working in the Biome app. The Biome app is a collection of data sources where a data source is a profiled website targeted specifically
    at cancer research. The user can add new data sources or may ask you to browser the data sources and return relevant datasets or other info. An example
    of a flow could be looking through all the data sources, picking one, finding a dataset using the URL, and then finally loading that dataset into a pandas
    dataframe.

    You must be extremely careful about what you print to stdout when running code--be cognizant of the size and make sure you don't print out huge things!
    Never, ever just print out the entire result of a workload or API search result. Always slice it and show just a subset to the user. You can save it as a variable
    for later use, etc.

    When you use a tool you must ALWAYS indicate which tool you are using by explicitly stating the tool name in your thinking. Wrap the tool name in backticks.
    You do not need to include the class name, just the method. For example you should not indicate `BiomeAgent.draft_api_code` but rather just `draft_api_code`.

    A very common workflow is to use the `draft_api_code` tool or the `consult_api_docs` tool to get code to interact with an API. 
    Once you have the code, you can use the `BiomeAgent__run_code` tool to execute the code.

    You will often be asked to integrate information from multiple sources to answer a question. For example, you may be asked to find a dataset
    from one API and integrate it with information from another API. In this case, you should be explicit about the steps needed to accomplish the task
    and where the information from each API is used. When you summarize your findings or results you should be clear about which information
    came from which API.
    """

    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
        self.root_folder = pathlib.Path(__file__).resolve().parent

        api_config = load(f'{self.root_folder}/api_agent.yaml')
        drafter_config = api_config["drafter_config"]
        finalizer_config = api_config["finalizer_config"]
        specs = api_config["api_specs"]

        super().__init__(context, tools, **kwargs)
        sleep(5)
        
        # Configure root logger
        logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
        
        self.logger = MessageLogger(self.context)

        # Add a direct console log to debug
        logger.info(f"drafter config (root logger): {drafter_config}")

        try:
            self.api = AdhocApi(logger=self.logger, drafter_config=drafter_config, finalizer_config=finalizer_config, apis=specs)
        except ValueError as e:
            self.add_context(f"The APIs failed to load for this reason: {str(e)}. Please inform the user immediately.")
            self.api = None

        self.add_context(f"The APIs available to you are: \n{[spec['name'] for spec in specs]}")


    async def auto_context(self):
        return """You are an assistent that is intended to assist users various biomedical information tasks. You may be asked to 
        help them choose which APIs to use or to help them query them. 

        You must NEVER print out the entire result of a workload or API search result. Always slice it and show just a subset to the user. You can save it as a variable
        for later use, etc. Be extremely CAREFUL about this.

        If you need to print something, be extremely CAREFUL--don't print the whole thing!

        You must ALWAYS indicate which tool you are using by explicitly stating the tool name in your thinking. Wrap the tool name in backticks.

        Users may ask you to load and munge data and many other tasks.
        Try to identify all of the steps needed, and all of the tools. Assume the user wants to do all of the steps at once.
        
        If the user asks to extract something from a set of documents, you can use the Palimpzest family of tools to do this. First, generate a schema for the extraction. 
        Then, if necessary filter the data to only include the relevant documents. Next, convert the dataset to the schema that was generated. 
        Finally, execute the workload to extract the information from the dataset. You may need to use multiple tools to accomplish this, including the ability to 
        register datasets, setting the input source, filtering datasets, convert datasets, generating schemas, and executing workloads.

        Make sure you understand all the steps needed to complete the task. Try to run all of the steps at once.

        If the results of a API search yields no results, you should use the `consult_api_docs` tool to check that you are querying the API correctly.
        """        

    @tool()
    async def draft_api_code(self, api: str, goal: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        """
        Drafts python code for an API request given a specified goal, such as a query for a specific study. You can use this tool to 
        get code to interact with the APIs that are available to you. When the user asks you to use an API and you are unsure how to do so, you should
        be sure to use this tool. Once you've learned how to do common tasks with an API you may not need this tool, but for accomplishing
        new tasks, you should use this tool. 
        
        The way this tool functions is that it will provide the goal to an external agent, which we refer to as the "drafter". 
        The drafter has access to the API documentation for the API in question. The drafter will then generate the code to perform the desired operation. 
        However, the drafter requires a very specific goal in order to do their job and does not have the ability to guess or infer. 
        Therefore, you must provide a very specific goal. It also does not have awareness of information outside of what you provide in the goal. 
        Therefore, if you have run code previously that returned information such as names of studies, `ids` of datasets, etc, you must provide that 
        information in the goal if it is needed to perform the desired operation.

        If you are asked to query for something specific, e.g. a study, you MUST provide the relevant `id` as part of the goal if you have access to it.
        Most APIs allow you to easily query by `id` so this is often possible to utilize.
        For example, if you are asked to find a dataset and you have the `id` of the dataset, you should provide that in the goal.
        Be as SPECIFIC as possible as this will help you get a more accurate and timely result. Do not be vague, provide
        VERBOSE goals so that the drafter of the code has all the information needed to do their job.

        The code that is drafted will generally be a complete, small program including relevant imports and other boilerplate code. Much of this 
        may already be implemented in the code you have run previously; if that is the case you should not repeat it. Feel free to streamline the code
        generated by removing any unnecessary steps before sending it to the `BiomeAgent__run_code` tool.

        You may want to use the consult_api_docs tool to ask questions of the API before running this tool to help refine your goal!

        If you use this tool, you MUST indicate so in your thinking. Wrap the tool name in backticks. 
        
        You MUST also be explicit about the goal in your thinking.

        Args:
            api (str): The name of the API to use
            goal (str): The task to be performed by the API request. This should be as specific as possible and include any relevant details such as the `ids` or other parameters that should be used to get the desired result.

        Returns:
            str: Depending on the user defined configuration will do one of two things.
                 Either A) return the raw generated code. Or B) Will attempt to run the code and return the result or
                 any errors that occurred (along with the original code). if an error is returned, you may consider
                 trying to fix the code yourself rather than reusing the tool.
        """
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
    async def consult_api_docs(self, api: str, query: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        """
        This tool is used to ask a question of an API. It allows you to ask a question of an API's documentation and get results in
        natural language, which may include code snippets or other information that you can then use to write code to interact with the API 
        (e.g. using the `BiomeAgent__run_code` tool). You can also use this information to refine your goal when using the `draft_api_code` tool.

        You can ask questions related to endpoints, payloads, etc. For example, you can ask "What are the endpoints for this API?"
        or "What payload do I need to send to this API?" or "How do I query for datasets by keyword?" etc, etc.

        If you use this tool, you MUST indicate so in your thinking. Wrap the tool name in backticks.

        Args:
            api (str): The name of the API to use
            query (str): The question you want to ask about the API.

        Returns:
            str: returns instructions on how to utilize the API based on the question asked.
        """
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
        For the Biome agent, you should use this tool to execute code in the user's notebook on behalf of the user, 
        but collects the outputs of the run for use by the Agent in the ReAct loop, if needed. Don't use the base `run_code` tool, 
        use this one instead.

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


    @tool
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
    
    @tool()
    async def add_example(self, api: str, code: str, description: str) -> str:
        """
        Add a successful code example to the API's examples.md documentation file.
        This tool should be used after successfully completing a task with an API to capture the working code for future reference.

        Args:
            api (str): The name of the API the example is for
            code (str): The working, successful code to add as an example
            description (str): A brief description of what the example demonstrates

        Returns:
            str: Message indicating success or failure of adding the example
        """
        try:
            # Construct path to examples.md file
            examples_path = os.path.join(self.root_folder, api, "api_definitions", "documentation", "examples.md")
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
                f.write(f"\n## Example {example_num}: {description}\n\n")
                f.write("```\n")
                f.write(code)
                f.write("\n```\n")

            return f"Successfully added example {example_num} to {examples_path}"

        except Exception as e:
            self.logger.error(str(e))
            return f"Failed to add example: {str(e)}"