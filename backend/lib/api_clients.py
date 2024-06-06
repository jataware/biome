from lib.settings import settings
from openai import OpenAI
from redis import Redis
from elasticsearch import Elasticsearch


def get_redis(host=None, port=None) -> Redis:
    return Redis(
        host=host or "sources_rq_redis",
        port=port or 6379,
    )

def get_openai(api_key=None, org_id=None) -> OpenAI:
    return OpenAI(
        api_key=api_key or settings.OPENAI_API_KEY,
        organization=org_id or settings.OPENAI_ORG_ID,
    )

def get_elastic(host=None, port=None, user=None, passwd=None) -> Elasticsearch:
    es_str = "http://"

    if (user or settings.ES_USER) and (passwd or settings.ES_PASS): 
        es_str = f"{es_str}{user or settings.ES_USER}:{passwd or settings.ES_PASS}@"

    es_str = f"{es_str}{host or settings.ES_HOST}:{port or settings.ES_PORT}"

    return Elasticsearch(es_str)


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