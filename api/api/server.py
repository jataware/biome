from fastapi import FastAPI  # , HTTPException, status
import logging
import json
from pydantic import BaseModel
from os import environ
from rq import Queue, Retry
from redis import Redis
from typing import Optional, List
from .settings import settings

from elasticsearch import Elasticsearch

from fastapi import APIRouter, File, HTTPException, Query, Response, UploadFile, status, Request
from fastapi.middleware.cors import CORSMiddleware


es = Elasticsearch(
    [
        {
            "scheme": "http", # TODO env, or include with url var below
            "host": settings.ELASTICSEARCH_URL,
            "port": settings.ES_PORT,
        }
    ]
)


logger = logging.getLogger(__name__)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO copy Dojo's setup that creates es indeces if missing?

redis = Redis(
    environ.get("REDIS_HOST", "sources_rq_redis.sources"),
    environ.get("REDIS_PORT", "6379"),
)
q = Queue(connection=redis, default_timeout=-1)


@app.get("/")
def index():
    logger.info("Get test route.")
    return {"hello": "sources is ready"}

def add_id(hit):
    return {
        **hit["_source"],
        "id": hit["_id"]
    }

def format_source(source_obj):
    return add_id(source_obj)


@app.get("/sources")
def list_sources():
    logger.info("Getting all registered sources")
    
    q = {
        "query": {
            "match_all": {}
        }
    }

    size = 20 # for now hardcoded

    try:
        results = es.search(index="datasources", body=q, scroll="2m", size=size)
    except Exception as e:
        logger.exception(e)
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        raise e

    totalDocsInPage = len(results["hits"]["hits"])

    logger.info(f"Got {totalDocsInPage} results")

    if totalDocsInPage < size:
        scroll_id = None
    else:
        scroll_id = results.get("_scroll_id", None)
    
    return {
        "count": results["hits"]["total"]["value"],
        "items_in_page": totalDocsInPage,
        "sources": [format_source(i)
                    for i in results["hits"]["hits"]],
        "scroll_id": scroll_id
    }


@app.post("/add-force-source")
async def add_source_from_payload(request: Request):
    # TODO
    json_req = await request.json()

    body = json.dumps(json_req)

    es.index(index="datasources", body=body)

    return {"success": True}


class ExtractArgs(BaseModel):
    uris: List[str]
    name: str

@app.post("/scan")
def gpt_scan_uri(payload: ExtractArgs):
    logger.info(f"Queueing scan fn, uris: {payload.uris}")

    job = q.enqueue_call(
        func="workers.scan_uri_job.start",
        args=[payload.name, payload.uris[0]],
        retry=Retry(max=3, interval=[10, 30, 60]),
    )

    # TODO instead of returning ID, maybe start stream and
    # poll here but stream to client as things are ready..

    return {"queued": True, "job_id": job.id}
