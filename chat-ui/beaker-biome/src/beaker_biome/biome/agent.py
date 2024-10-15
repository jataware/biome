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

from .cache import APICache
import pathlib
import re

logger = logging.getLogger(__name__)

BIOME_URL = "http://biome_api:8082"

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
    """
    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        root_folder = pathlib.Path(__file__).resolve().parent
        self.cache = APICache(f'{root_folder}/api_agent.yaml')
        super().__init__(context, tools, **kwargs)
        self.add_context(f"The APIs available to you are: \n{self.cache.available_api_context()}")
        sleep(5)
    def gemini_info(self, info: dict):
        self.context.send_response("iopub",
            "gemini_info", {
                "body": info
            },
        ) 
    
    def gemini_error(self, error: dict):
        self.context.send_response("iopub",
            "gemini_error", {
                "body": error
            },
        ) 

    @tool()
    async def dump_cache(self):
        """
        This tool dumps the API cache to the user.
        """
        self.gemini_info({'config': str(self.cache.config), 'cache': str(self.cache.cache)})

    @tool()
    async def use_api(self, api: str, goal: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        """
        This tool provides interaction with external APIs with a second agent.
        You will query external APIs through this tool.
        Based on what that code returns and the user's goal, continue to interact with the API to get to that goal.

        The output will either be a summary of the code output or an error. 
        If it is an error, instruct the second agent to fix the code and retry.

        Consult the APIs available to you when specifying which to use.

        Continue to use the `use_api` tool until finished. 

        Args:
            api (str): The API to query. Must be one of the available APIs.
            goal (str): The task given to the second agent. If the user states the API is unauthenticated, relay that information here.
        Returns:
            str: A summary of the current step being run, along with the collected stdout, stderr, returned result, display_data items, and any
                 errors that may have occurred, or just an error.
              
        """
        self.gemini_info({'api': api, 'goal': goal})

        if api not in self.cache.loaded_apis():
            self.gemini_info({'cache': f'api is not loaded: {api}'})
            if api not in self.cache.available_apis():
                self.gemini_info({'cache': f'api does not exist: {api}'})
                return f"The selected API was not in the following list: {self.cache.available_apis()}. Please use one of those."
            self.gemini_info({'cache': f'loading api: {api}'})
            self.cache.load_api(api)
            
        try:
            agent_response = self.cache.chats[api].send_message(goal).text
            prefixes = ['```python', '```']
            suffixes = ['```', '```\n']
            for prefix in prefixes:
                if agent_response.startswith(prefix):
                    agent_response = agent_response[len(prefix):]
            for suffix in suffixes:
                if agent_response.endswith(suffix):
                    agent_response = agent_response[:-len(suffix)]
            agent_response = '\n'.join([
                'import pandas as pd',
                'import os',
                'import json',
                'import requests',
                agent_response
            ])
        except Exception as e:
            self.gemini_error({'error': str(e)})
            return f"The agent failed to produce valid code: {str(e)}"

        transformed_code = agent_response

        def remove_whitespace(code: str) -> str:
            return re.sub(r'\s+', '', str(code))

        try:
            syntax_check_prompt = self.cache.config.get('syntax_check_prompt','')
            if syntax_check_prompt != '':
                transformed_code = await agent.query(syntax_check_prompt.format(code=transformed_code))
                if remove_whitespace(transformed_code) != remove_whitespace(agent_response):
                    self.gemini_info({
                        "message": "GPT has changed the code output from Gemini in the syntax fix step.", 
                        "gpt": transformed_code, 
                        "gemini": agent_response
                    })
        except Exception as e:
            self.gemini_error({'error': str(e)})
            return f"""
                The second agent failed to create valid code. Instruct it to rerun. The error was {str(e)}. The code will be provided for fixes or retry.
                """
        try:
            additional_pass_prompt = self.cache.cache[api].get('gpt_additional_pass', '')
            if additional_pass_prompt != '':
                prior_code = transformed_code
                transformed_code = await agent.query(
                    additional_pass_prompt.format_map(self.cache.cache[api] | {'code': transformed_code})
                )
                if remove_whitespace(transformed_code.strip) != remove_whitespace(prior_code.strip()):
                    self.gemini_info({
                        "message": "GPT has changed the code output from Gemini or the syntax check in the additional pass step.", 
                        "gpt": transformed_code, 
                        "prior": prior_code
                    })
        except Exception as e:
            self.gemini_error({'error': str(e)})
            return f"""
                The second agent failed to create valid code. Instruct it to rerun. The error was {str(e)}. The code will be provided for fixes or retry.
                """
        

        try:
            self.gemini_info({'tools': str(agent.tools)})
            evaluation = await self.tools['BiomeAgent.run_code2'](transformed_code, agent, loop, react_context)
        except Exception as e:
            self.gemini_error({'error': str(e)})
            return f"""
                The second agent failed to create valid code. Instruct it to rerun. The error was {str(e)}. The code will be provided for fixes or retry.
                """
        self.gemini_info({"eval": str(evaluation), "type": str(type(evaluation))})
        return evaluation
    

    @tool()
    async def run_code2(self, code: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        """
        Executes code in the user's notebook on behalf of the user, but collects the outputs of the run for use by the Agent
        in the ReAct loop, if needed.

        The code runs in a new codecell and the user can watch the execution and will see all of the normal output in the
        Jupyter interface.

        This tool can be used to probe the user's environment or collect information to answer questions, or can be used to
        run code completely on behalf of the user. If a user asks the agent to do something that reasonably should be done
        via code, you should probably default to using this tool.

        This tool can be run more than once in a react loop. All actions and variables created in earlier uses of the tool
        in a particular loop should be assumed to exist for future uses of the tool in the same loop.

        Args:
            code (str): Code to run directly in Jupyter. This should be a string exactly as it would appear in a notebook
                        codecell. No extra escaping of newlines or similar characters is required.
        Returns:
            str: A summary of the run, along with the collected stdout, stderr, returned result, display_data items, and any
                errors that may have occurred.
        """
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

        self.gemini_info({'ctx': str(execution_context)})

        return format_execution_context(execution_context)

    # def update_job_status(self, job_id, status):
    #     self.context.send_response("iopub", 
    #             "job_status", {
    #                 "job_id": job_id,
    #                 "status": status 
    #             },
    #         )

    # # TODO: Formatting of these messages should be left to the Analyst-UI in the future. 
    # async def poll_query(self, job_id: str):
    #     # Poll result
    #     status = "queued"
    #     result = None
    #     while status == "queued":
    #         response = requests.get(f"{BIOME_URL}/jobs/{job_id}").json()
    #         status = response["status"]
    #         sleep(1)
        
    #     self.update_job_status(job_id, status)

    #     #asyncio.create_task(self.poll_query_logs(job_id))
    #     while status == "started":
    #         response = requests.get(f"{BIOME_URL}/jobs/{job_id}/logs").json()
    #         self.context.send_response("iopub",
    #             "job_logs", {
    #                 "job_id": job_id,
    #                 "logs": response,
    #             },
    #         )
    #         response = requests.get(f"{BIOME_URL}/jobs/{job_id}").json()
    #         status = response["status"]
    #         sleep(5)

    #     self.update_job_status(job_id, status)

    #     # Handle result
    #     if status != "finished":
    #         self.update_job_status(job_id, status)
    #         self.context.send_response("iopub", 
    #             "job_failure", {
    #                 "job_id": job_id,
    #                 "response": response
    #             },
    #         ) 

    #     result = response["result"] # TODO: Bubble up better cell type
    #     self.context.send_response("iopub",
    #         "job_response", {
    #             "job_id": job_id,
    #             "response": result['answer'],
    #             "raw": result
    #         },
    #     ) 

    # @tool(autosummarize=True)
    # async def search(self, query: str) -> list[dict[str, Any]]:
    #     """
    #     Search for data sources in the Biome app. Results will be matched semantically
    #     and string distance. Use this to find a data source. You don't need live
    #     web searches. If the user asks about data sources, use this tool.

    #     Be sure to use the `display_search` tool for the output. Ensure you always use `display_search` after.

    #     Args:
    #         query (str): The query used to find the datasource.
    #     Returns:
    #         list: A JSON-formatted string containing a list of strings.
    #               The list should contain only the `name` field and no other field
    #               of the data sources found, ordered from most relevant to least relevant.
    #               Ensure that only the name field is present.
    #               An example is provided surrounded in backticks.
    #               ```
    #               ["Proteomics Data Commons", ""Office of Cancer Clinical Proteomics Research", "UniProt"]
    #               ```
    #     """

    #     endpoint = f"{BIOME_URL}/sources"
    #     response = requests.get(endpoint, params={"query": query})
    #     raw_sources = response.json()['sources']
    #     sources = [
    #         # Include only necessary fields to ensure LLM context length is not exceeded.
    #         {
    #             "id": source["id"],
    #             "name": source["content"]["Web Page Descriptions"]["name"],
    #             "initials": source["content"]["Web Page Descriptions"]["initials"],
    #             "purpose": source["content"]["Web Page Descriptions"]["purpose"],
    #             "links": source["content"]["Information on Links on Web Page"],
    #             "base_url": source.get("base_url", None)
    #         } for source in raw_sources
    #     ]
    #     return sources

    # @tool(autosummarize=True)
    # async def display_search(self, results: list[str], agent:AgentRef, loop: LoopControllerRef):
    #     """
    #     Once search has been performed, this tool will display it to the user.
    #     Args:
    #         results (list[str]): The query used to find the datasource.
    #     """
    #     # sometimes it wraps the output
    #     if isinstance(results, dict):
    #         results = results.get("results", results)
    #     endpoint = f"{BIOME_URL}/sources"
    #     response = requests.get(endpoint, params={
    #         "simple_query_string": {
    #             "fields": ["content.Web Page Descriptions.name"],
    #             "query": "|".join(results)
    #         }
    #     })
    #     raw_sources = response.json()['sources']
    #     sources = [
    #         {
    #             "id": source["id"],
    #             "name": source["content"]["Web Page Descriptions"]["name"],
    #             "initials": source["content"]["Web Page Descriptions"]["initials"],
    #             "purpose": source["content"]["Web Page Descriptions"]["purpose"],
    #             "links": source["content"]["Information on Links on Web Page"],
    #             "base_url": source.get("base_url", None),
    #             "logo": source.get("logo", None)
    #         } for source in raw_sources
    #     ]
    #     # match sources to ordering from previous llm step by dict to avoid n^2

    #     sources_map = { source.get("name", ""): source for source in sources }
    #     ordered_sources = [sources_map[name] for name in results]
    #     self.context.send_response("iopub",
    #         "data_sources", {
    #             "sources": ordered_sources
    #         },
    #     )
    #     loop.set_state(loop.STOP_SUCCESS)

    # # TODO(DESIGN): Deal with long running jobs in tools
    # #
    # # Option 1: We can return the job id and the agent can poll for the result.
    # # This will require a job status tool. Once the status is done, we can either
    # # check the result if it's a query or check the data source if it's a scan.
    # # This feels a bit messy though that the job creation has a similar return
    # # output on queue but getting the result is very different for each job.
    # #
    # # Option 2: We can wait for the job and return it to the agent when it's done
    # #
    # # Option 3: We can maybe leverage new widgets in the Analyst UI??
    # #

    # # CHOOSING OPTION 1 FOR THE TIME BEING
    # @tool()
    # async def query_page(self, task: str, base_url: str, agent: AgentRef, loop: LoopControllerRef):
    #     """
    #     Run an action over a *specific* source in the Biome app and return the results.
    #     Find the url from a data source by using `search` tool first and
    #     picking the most relevant one.

    #     This kicks off a long-running job so you'll have to just return the ID to the user
    #     instead of the result. 

    #     This can be used to ask questions about a data source or download some kind
    #     of artifact from it. This tool just kicks off a job where an AI crawls the website
    #     and performs the task.

    #     Args:
    #         task (str): Task given in natural language to perform over URL.
    #         base_url (str): URL to run query over.
    #     """
    #     response = requests.post( f"{BIOME_URL}/jobs/query", json={"user_task": task, "url": base_url})
    #     job_id = response.json()["job_id"]
    #     self.context.send_response("iopub",
    #         "job_create", {
    #             "job_id": job_id,
    #             "task": task,
    #             "url": base_url
    #         },
    #     )
    #     asyncio.create_task(self.poll_query(job_id))
    #     loop.set_state(loop.STOP_SUCCESS)

    # @tool()
    # async def scan(self, base_url: str, agent:AgentRef, loop: LoopControllerRef) -> str:
    #     """
    #     Profiles the given web page and adds it to the data sources in the Biome app.

    #     This kicks off a long-running job so you'll have to just return the ID to the user
    #     instead of the result. 

    #     Args:
    #         base_url (str): The url to scan and add as a data source.
    #     Returns:
    #         str: Job ID to poll for the result. 
    #     """
    #     response = requests.post( f"{BIOME_URL}/jobs/scan", json={"uris": [base_url]})
    #     job_id = response.json()["job_id"]
    #     asyncio.create_task(self.poll_query(job_id))
    #     return job_id
