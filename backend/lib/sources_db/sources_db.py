import json
import logging
from typing import Callable
from dataclasses import dataclass

from elasticsearch import Elasticsearch
from openai import OpenAI

from lib.settings import settings

PRIMARY_INDEX = "datasources"
PRIMARY_INDEX_SCHEMA = "/backend/lib/sources_db/datasources_schema.json"
PRIMARY_INDEX_SEEDS = "/backend/api/seeds.json"
CACHE_INDEX = "cache"
RESULT_MAX_SIZE = 100

logger = logging.getLogger(__name__)

def get_embedding(text: str) -> list[float]:
    cleaned_text = text.replace("\n", " ")
    client_response = OpenAI().embeddings.create(
        input=cleaned_text, 
        model="text-embedding-3-small"
    )
    return client_response.data[0].embedding

@dataclass
class SearchResult:
    """
    SearchResult class to store and scroll search results.
    """
    total : int
    sources : list[dict]
    scroll : Callable[[], "SearchResult"] | None

class SourcesDatabase:
    """
    Data Source Storage class to store and search over datasources.

    Storage acts as a singleton across the entire application. The
    expectation is that initializing this class will create a connection,
    therefore, creating a new instance in a separate runtime or container
    is trivial.
    """

    def __init__(self):
        """
        Initializes a connection to storage and will create and seed the
        necessary data if it does not already exist.

        Side effects:
            - Seeds data.
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
            logger.info("Seeding datasources")
            for source in json.load(open(PRIMARY_INDEX_SEEDS)):
                self.store(source)


    def store(self, source):
        """
        Store data source in the storage.

        Side effects:
         - Adds new source to DB.
         - Adds new elements `source` input with new key 'embedded_summary'.

        Args:
            source (dict): The data source to store in the storage.
        """
        # TODO: Remove workaround once upstream is fixed
        if isinstance(source["summary"], str):
            source["summary"] = json.loads(source["summary"])

        text = source["summary"]["summary"]
        embedded_summary = get_embedding(text)
        source["embedded_summary"] = embedded_summary
        body = json.dumps(source)
        self.es.index(index=PRIMARY_INDEX, body=body)

    
    def search(self, query: str | None = None, raw_query: str | dict | None = None) -> SearchResult:
        """
        Search data sources

        Args:
            query (str): The query to search for. If None, will return all data sources.
            raw_query (str): The raw elasticsearch query inside the `query` block to be performed. Ignored if None.

        Returns:
            SearchResult: The search result containing the total number of results and the sources.
        """
        if raw_query is not None:
            if isinstance(raw_query, str):
                raw_query = json.loads(raw_query)
            es_query = {
                "query": raw_query
            }
        elif query is None:
            es_query = {
                "query": {
                    "match_all": {}
                } 
            }
        else:
            embedded_query = get_embedding(query)
            es_query = {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "script_score": {
                                    "query": {"match_all": {}},
                                    "script": {
                                        "source": "return Math.max(cosineSimilarity(params.query_vector, 'embedded_summary'), 0)",
                                        "params": {
                                            "query_vector": embedded_query
                                        }
                                    },
                                },
                            },
                            {
                                "constant_score": {
                                    "filter": {
                                        "match": {
                                            "summary.summary": {
                                                "query": query,
                                                "fuzziness": 2
                                            }
                                        }
                                    },
                                    "boost": 1
                                }
                            },
                        ]
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

        return SearchResult(
            total = results["hits"]["total"]["value"],
            sources = sources,
            scroll = scroll,
        )

