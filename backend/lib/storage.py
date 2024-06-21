import json
import logging

from elasticsearch import Elasticsearch

from lib.settings import settings

PRIMARY_INDEX = "datasources"
PRIMARY_INDEX_SCHEMA = "/backend/api/datasources_schema.json"
PRIMARY_INDEX_SEEDS = "/backend/api/seeds.json"
CACHE_INDEX = "cache"
RESULT_MAX_SIZE = 20

logger = logging.getLogger(__name__)

class DataSourceStorage:
    """
    Data Source Storage class to store and search over datasources.
    """

    def __init__(self):
        # Environment variables ES_USER and ES_PASS are implicitly used here
        self.es =  Elasticsearch(
            [
                {
                    "scheme": "http",
                    "host": settings.ES_HOST,
                    "port": settings.ES_PORT,
                }
            ]
        )

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
                body = json.dumps(source)
                self.es.index(index=PRIMARY_INDEX, body=body)
        else:
            logger.info("No need to seed as it is not empty.")


    def store(self, source):
        body = json.dumps(source)
        self.es.index(index=PRIMARY_INDEX, body=body)
    
    def _process_results(self, results):
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

    
    def search(self, query: str | None = None):
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
  
