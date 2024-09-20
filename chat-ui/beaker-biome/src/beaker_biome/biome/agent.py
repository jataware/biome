import json
import logging
import re
import requests
from time import sleep
import asyncio

from archytas.tool_utils import AgentRef, LoopControllerRef, ReactContextRef, tool
from typing import Any

from beaker_kernel.lib.agent import BaseAgent
from beaker_kernel.lib.context import BaseContext

import google.generativeai as genai
from google.generativeai import caching

logger = logging.getLogger(__name__)

BIOME_URL = "http://biome_api:8082"

disease_types = """
- adenomas and adenocarcinomas
- ductal and lobular neoplasms
- myeloid leukemias
- epithelial neoplasms, nos
- squamous cell neoplasms
- gliomas
- lymphoid leukemias
- cystic, mucinous and serous neoplasms
- nevi and melanomas
- neuroepitheliomatous neoplasms
- acute lymphoblastic leukemia
- plasma cell tumors
- complex mixed and stromal neoplasms
- mature b-cell lymphomas
- transitional cell papillomas and carcinomas
- not applicable
- osseous and chondromatous neoplasms
- germ cell neoplasms
- mesothelial neoplasms
- not reported
- acinar cell neoplasms
- paragangliomas and glomus tumors
- chronic myeloproliferative disorders
- neoplasms, nos
- thymic epithelial neoplasms
- myomatous neoplasms
- complex epithelial neoplasms
- soft tissue tumors and sarcomas, nos
- lipomatous neoplasms
- meningiomas
- fibromatous neoplasms
- specialized gonadal neoplasms
- unknown
- miscellaneous tumors
- adnexal and skin appendage neoplasms
- basal cell neoplasms
- mucoepidermoid neoplasms
- myelodysplastic syndromes
- nerve sheath tumors
- leukemias, nos
- synovial-like neoplasms
- fibroepithelial neoplasms
- miscellaneous bone tumors
- blood vessel tumors
- mature t- and nk-cell lymphomas
- _missing
"""

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
    GDC_MODEL_DISPLAY_NAME='GDC_CACHE_API_DOCS'
    GDC_MODEL='models/gemini-1.5-flash-001'
    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        import os
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.gemini = {}
        super().__init__(context, tools, **kwargs)
        self.try_load_cache()

    def try_load_cache(self):
        content = caching.CachedContent.list()
        is_cached = False
        for cache_object in content: 
            if cache_object.display_name == self.GDC_MODEL_DISPLAY_NAME:
                is_cached = True 
                break
        if not is_cached:
            self.gemini_info({"cache": "Cache was not found."})
            cache_object = self.build_cache()
        else:
            self.gemini_info({"cache": "Cache was found."})
        self.gemini['model'] = genai.GenerativeModel.from_cached_content(cached_content=cache_object)
        self.gemini['chat'] = self.gemini['model'].start_chat()

    def build_cache(self):
        import pathlib
        import datetime
        agent_dir = pathlib.Path(__file__).resolve().parent
        with open(f'{agent_dir}/docs.md', 'r') as f:
            docs = f.read()

        prompt = """
        You are an assistant who will help me query the genomics data commons API.
        You should write clean python code to solve specific queries I pose. You should 
        write it as though it will be directly used in a Jupyter notebook. You should not 
        include backticks or "python" at the top of the code blocks, that is unnecessary.
        You should not provide explanation unless I ask a follow up question.
        Assume pandas is installed and is imported with `import pandas as pd`. Also assume `requests`, `json`, 
        and `os` are imported properly.
        """

        cached_content = f"""
        You will be given the entire API documentation, but first I want to give you a list of available 
        disease types since this is a common search parameter: 

        {disease_types}

        If you are specifying a disease type, it MUST be from this enumerated list.

        Now, I will provide you the extensive API documentation. When you write code against this API
        you should avail yourself of the appropriate query parameters, your understanding of the response model
        and be cognizant that not all data is public and thus may require a token, etc. When you are downloading
        things you should log progress. When you are doing complex things try to break them down and 
        implement appropriate exception handling. Ok here we go, here are the docs: 

        Unless you receive a 403 forbidden, assume the endpoints are unauthenticated.
        If the user says the API does not require authentication, OMIT code about tokens and token handling and token headers.
        
        {docs}
        """
        cache = caching.CachedContent.create(
            model=self.GDC_MODEL,
            display_name=self.GDC_MODEL_DISPLAY_NAME,
            contents=[cached_content],
            ttl=datetime.timedelta(days=30),
            system_instruction=prompt
        )
        return cache

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
    async def interact_with_api(self, goal: str, agent: AgentRef, loop: LoopControllerRef, react_context: ReactContextRef) -> str:
        """
        This tool provides interaction with external APIs with a second agent.
        You will query external APIs through this tool.
        Based on what that code returns and the user's goal, continue to interact with the API to get to that goal.

        The output will either be a summary of the code output or an error. 
        If it is an error, instruct the second agent to fix the code and retry.

        Args:
            goal (str): The task given to the second agent. If the user states the API is unauthenticated, relay that information here.
        Returns:
            str: A summary of the current step being run, along with the collected stdout, stderr, returned result, display_data items, and any
                 errors that may have occurred, or just an error.
              
        """
        self.gemini_info({'goal': goal})
        try:
            agent_response = self.gemini['chat'].send_message(goal).text
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
        
        fixed_code = await agent.query(f"""The code you received is will be listed below the line of dashes.
Please fix the python code for syntax errors and only return the python code with fixed syntax errors.
Ensure the output has no formatting and return just the code, please.

If the output has formatting like backticks or a language specifier, be sure to remove all formatting
and return nothing but the code itself with no additional text.
                                       
Example:
    Input:
        ```python
        print(a)
        ```
    Output:
        print(a)
    Input:
        ```python
        de f fn_b(b):
            print(this is an unescaped string)
        def fn_a(a):
            print(a)
        ```
        This code has been fixed to correctly solve the task.
    Output:
        def fn_b(b):
            print("this is an unescaped string")
        def fn(a):
            print(a)
                    
----------

{agent_response}
""")
        self.gemini_info({'syntax_check_output': fixed_code})
        try:
            evaluation = await agent.tools['run_code'](fixed_code, agent, loop, react_context)
        except Exception as e:
            self.gemini_error({'error': str(e)})
            return f"""
                The second agent failed to create valid code. Instruct it to rerun. The error was {str(e)}. The code will be provided for fixes or retry.
                """
        return evaluation
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
