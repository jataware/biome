from elasticsearch import Elasticsearch
from workers.settings import settings
from openai import OpenAI


def get_elasticsearch(scheme=None, host=None, port=None) -> Elasticsearch:
    return Elasticsearch(
        [
            {
                "scheme": scheme or "http",
                "host": host or settings.ELASTICSEARCH_URL,
                "port": port or settings.ELASTICSEARCH_PORT,
            }
        ]
    )


def get_openai(api_key=None, org_id=None) -> OpenAI:
    return OpenAI(
        api_key=api_key or settings.OPENAI_API_KEY,
        organization=org_id or settings.OPENAI_ORG_ID,
    )
