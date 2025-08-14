import logging
import requests
import os

from archytas.tool_utils import AgentRef, LoopControllerRef, ReactContextRef, tool
from typing import List

from beaker_kernel.lib.agent import BeakerAgent
from beaker_kernel.lib.context import BaseContext

from pathlib import Path

from Bio import Entrez

from biome.literature_review import LiteratureReviewAgent, PubmedSource

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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


class BiomeAgent(BeakerAgent):
    """
    You are the Biome Agent, a chat assistant that helps users with biomedical research tasks.

    An 'integration' is defined as an API or dataset or general collection of knowledge that you have access to.

    An API should be considered a type of integration.
    """
    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        lit_review_dir_raw = os.environ.get("BIOME_LIT_REVIEW_DIR", "./_literature_review")
        try:
            lit_review_dir = Path(lit_review_dir_raw).resolve(strict=True)
        except OSError as e:
            lit_review_dir = Path('.') / lit_review_dir_raw
            lit_review_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"Using lit review directory: {lit_review_dir}")
        self.lit_review_dir = lit_review_dir

        self.initialize_literature_review()
        self.initialize_entrez()

        self.logger = MessageLogger(self.log, logger)
        super().__init__(context, tools, **kwargs)

    def initialize_literature_review(self):
        self.litreview_agent = LiteratureReviewAgent(self.lit_review_dir)
        self.litreview_agent.add_source("pubmed", PubmedSource())

    def initialize_entrez(self):
        if (entrez_email := os.environ.get("ENTREZ_EMAIL", None)):
            Entrez.email = entrez_email
        if (entrez_key := os.environ.get("ENTREZ_API_KEY", None)):
            Entrez.api_key = entrez_key

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
