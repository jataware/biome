import json
import logging
from typing import Callable
from dataclasses import dataclass

from elasticsearch import Elasticsearch
from openai import OpenAI

from lib.settings import settings

PRIMARY_INDEX = "datasources"
PRIMARY_INDEX_SCHEMA = "/backend/lib/storage/datasources_schema.json"
PRIMARY_INDEX_SEEDS = "/backend/api/seeds.json"
CACHE_INDEX = "cache"
RESULT_MAX_SIZE = 20

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    total : int
    sources : list[dict]
    scroll : Callable[[], "SearchResult"] | None

class DataSourceStorage:
    """
    Data Source Storage class to store and search over datasources.

    Storage acts as a singleton across the entire application. The
    expectation is that initializing this class will create a connection,
    therefore
    """

    def __init__(self):
        """
        Initializes a connection to storage and will create and seed the
        necessary data if it does not already exist.
        """
        # NOTE: Environment variables ES_USER and ES_PASS are implicitly used here
        self.es =  Elasticsearch(
            [
                {
                    "scheme": "http",
                    "host": settings.ES_HOST,
                    "port": settings.ES_PORT,
                }
            ]
        )

        ### Elasticsearch Index Initialization ###
        if not self.es.indices.exists(index=PRIMARY_INDEX):
            logger.info(f"Creating index {PRIMARY_INDEX}")
            mappings = json.load(open(PRIMARY_INDEX_SCHEMA))["mappings"]
            self.es.indices.create(index=PRIMARY_INDEX, body={}, mappings=mappings)   
        
        logger.info(f"Checking if {PRIMARY_INDEX} should be seeded.")
        all_query = {"query": {"match_all": {}}}

        results = self.es.search(index=PRIMARY_INDEX, body=all_query)
        count = results["hits"]["total"]["value"]

        if count == 0:
            logger.info("Need to seed index as it is empty.")
            logger.info("Seeding datasources")
            for source in json.load(open(PRIMARY_INDEX_SEEDS)):
                self.store(source)
        else:
            logger.info("No need to seed as it is not empty.")


    def store(self, source):
        body = json.dumps(source)
        self.es.index(index=PRIMARY_INDEX, body=body)
    
    def search(self, query: str | None = None) -> SearchResult:
        es_query = {
            "query": {
                "match_all": {}
            } if query is None else {
                "multi_match": {
                    "query": query,
                    "fields": ["Web Page Description", "summary"]
                }
            }
        }
        results = self.es.search(index=PRIMARY_INDEX, body=es_query, scroll="2m", size=RESULT_MAX_SIZE)
        return self._process_results(results)
 
    def _process_results(self, results) -> SearchResult:
        total_docs_in_page = len(results["hits"]["hits"])

        logger.info(f"Got {total_docs_in_page} results")

        if total_docs_in_page < RESULT_MAX_SIZE:
            scroll = None
        else:
            scroll_id = results.get("_scroll_id", None)
            def scroll():
                result = self.es.scroll(scroll_id=scroll_id, scroll="2m")
                return self._process_results(result)

        sources = [ 
            {**hit["_source"], "id": hit["_id"]}
            for hit in results["hits"]["hits"] 
        ]

        return {
            "total": results["hits"]["total"]["value"],
            "sources": sources,
            "scroll": scroll,
        }

    
