from lib.settings import settings
from openai import OpenAI
from redis import Redis
from elasticsearch import Elasticsearch


def get_elasticsearch(scheme=None, host=None, port=None) -> Elasticsearch:
    return Elasticsearch(
        [
            {
                "scheme": scheme or "http",
                "host": host or settings.ES_HOST,
                "port": port or settings.ES_PORT,
            }
        ]
    )