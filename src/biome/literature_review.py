from Bio import Entrez
from time import sleep
import os
import logging
import aiohttp
from paperqa.clients.unpaywall import UnpaywallProvider
from paperqa import Docs, Settings
from pathlib import Path
from typing import cast
import traceback
import json
import requests
from abc import ABC

logger = logging.getLogger(__name__)

class DocumentSource(ABC):
    # folder name for papers
    data_dir: str
    # set when added to LiteratureReviewAgent or manually
    qualified_path: Path | None
    async def fetch_for_query(self, query: str):
        """
        Fetch papers for a given query and write them to qualified_path.
        Returns details relevant for an agent to read, in an unspecified format.
        """
        ...


class LiteratureReviewAgent:
    source_root: Path
    source_dirs: list[str]
    sources: dict[str, DocumentSource]
    def __init__(self, source_root: Path):
        self.source_root = source_root
        self.source_dirs = []
        self.sources = {}
    def add_source(self, name: str, source: DocumentSource):
        self.source_dirs.append(source.data_dir)
        source.qualified_path = self.source_root / source.data_dir
        self.sources[name] = source
    async def fetch_for_query(self, source_name: str, query: str):
        return await self.sources[source_name].fetch_for_query(query)
    async def paperQA(self, query: str) -> str:
        """
        run paperQA over the downloaded corpus and returns the response
        """
        docs = Docs()
        settings = Settings(
            llm=os.getenv("PAPERQA_LLM_MODEL"),
            callbacks=["langsmith"]
        )
        for path in self.source_dirs:
            output_dir = self.source_root / path
            for paper in output_dir.glob('*.html'):
                await docs.aadd(paper)
            for paper in output_dir.glob('*.pdf'):
                await docs.aadd(paper)
        session = await docs.aquery(query, settings=settings)
        return str(session)


class PubmedSource(DocumentSource):
    def __init__(self, qualified_path=None):
        self.data_dir = "pubmed"
        self.qualified_path = qualified_path

    async def fetch_for_query(self, query: str):
        return await self.pubmed_search(query)

    def _assert_qualified_path(self) -> Path:
        if self.qualified_path is None:
            raise ValueError("Ensure qualified_path is set via initializer or from LiteratureReviewAgent.")
        return self.qualified_path

    def entrez_read(self, handle) -> dict:
        sleep(0.25) # rate limits - recommended by entrez docs
        results = Entrez.read(handle)
        handle.close()
        return results # type: ignore

    def pubmed_search_ids(self, query: str) -> list[str]:
        results = self.entrez_read(Entrez.esearch(db="pubmed", term=query, retmax=25))
        if (id_list := results.get("IdList", None)):
            return id_list
        return ["No IDs returned for the given query."]

    def get_pubmed_fulltext(self, pmc_id: str):
        """
        download the fulltext of a paper given a PMC id and save it to
        the agent's data dir for dataset storage.

        this operation is expected to fail gracefully and logs, rather than
        raising the exception further
        """
        try:
            text = []
            cursor = 0
            while True:
                response = Entrez.efetch(db="pmc", id=pmc_id, retstart=cursor, rettype="xml")
                sleep(0.25)
                body = cast(bytes, response.read()).decode('utf-8')
                text.append(body)
                if "[truncated]" in response or "Result too long" in body:
                    cursor += len(body)
                else:
                    break
            contents = "".join(text)
            output_dir = self._assert_qualified_path()
            fulltext_file = output_dir / f"{pmc_id}.fulltext.html"
            os.makedirs(str(output_dir), exist_ok=True)
            with open(fulltext_file, 'w') as f:
                f.write(contents)
            return contents
        except Exception:
            logger.error(traceback.print_exc())

    async def fetch_from_unpaywall(self, doi: str) -> str:
        """
        return the pdf link to a paper from unpaywall as a fallback method
        """
        try:
            async with aiohttp.ClientSession() as session:
                provider = UnpaywallProvider()
                details = await provider.get_doc_details(doi, session)
                return details.pdf_link
        except Exception:
            raise ValueError("No PDF link found.")

    async def pubmed_search(self, query: str):
        """
        search pubmed for papers given a query and download the respective papers.

        this tool includes downloading them, as fallbacks might catch papers not existing
        on PMC.
        """
        paper_ids = self.pubmed_search_ids(query)
        details = {}
        for paper_id in paper_ids:
            output_dir = self._assert_qualified_path()
            os.makedirs(str(output_dir), exist_ok=True)
            metadata_file = output_dir / f"{paper_id}.metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    details[paper_id] = json.load(f)
                    continue
            try:
                results = self.entrez_read(Entrez.efetch(db="pubmed", id=paper_id))
                date_revised_raw = results["PubmedArticle"][0]["MedlineCitation"]["DateRevised"]
                date_revised = "{}/{}/{}".format(
                    *[str(date_revised_raw[field])
                        for field in ["Year", "Month", "Day"]])
                try:
                    abstract = " ".join(results["PubmedArticle"][0]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
                except KeyError:
                    abstract = "<not found>"

                title = results["PubmedArticle"][0]["MedlineCitation"]["Article"]["ArticleTitle"]

                authors = list(filter(
                    lambda author: '<invalid>' not in author,
                    [
                        f"{author.get('ForeName', '<invalid>')} {author.get('LastName', '<invalid>')}"
                        for author in [
                            dict(author_data)
                            for author_data in results["PubmedArticle"][0]['MedlineCitation']['Article']['AuthorList']
                        ]
                    ]
                ))

                try:
                    doi = [
                        str(element) for element in
                        filter(
                            lambda xml_string: xml_string.attributes.get("IdType", None) == 'doi',
                            results["PubmedArticle"][0]['PubmedData']['ArticleIdList']
                        )
                    ][0]
                except IndexError:
                    doi = "<not found>"

                publication = results["PubmedArticle"][0]['MedlineCitation']['Article']['Journal']['Title']

                try:
                    related = self.entrez_read(Entrez.elink(dbfrom="pubmed", db="pmc", id=paper_id))
                    pmc_full_text = related[0]["LinkSetDb"][0]["Link"][0]["Id"]
                except Exception:
                    pmc_full_text = None
                    try:
                        pdf_url = await self.fetch_from_unpaywall(doi)
                        if pdf_url is not None:
                            response = requests.get(pdf_url)
                            response.raise_for_status()
                            output_dir = self._assert_qualified_path(self)
                            fulltext_file = output_dir / f"{doi}.fulltext.pdf"
                            with open(fulltext_file, 'w') as f:
                                f.write(response.text)
                    except Exception as e:
                        logger.warning(f"{doi} -- Failed to get fulltext location - not in pubmed OR unpaywall")

                paper_details = {
                    "date_revised": date_revised,
                    "title": title,
                    "abstract": abstract,
                    "doi": doi,
                    "authors": authors,
                    "publication": publication,
                    "pmc_full_text_id": pmc_full_text
                }
                details[paper_id] = paper_details
                with open(metadata_file, "w") as f:
                    json.dump(paper_details, f)
            except Exception:
                import traceback
                logger.warning(f"Failed to read paper: {paper_id}")
                logger.warning(traceback.print_exc())
                logger.warning(results)

        for paper_id in details:
            if (pmc_id := details[paper_id].get('pmc_full_text_id')) is not None:
                self.get_pubmed_fulltext(pmc_id)

        return details

