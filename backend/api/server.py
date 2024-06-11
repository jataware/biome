from fastapi import FastAPI, exceptions, Request  # HttpException, status
from fastapi.staticfiles import StaticFiles
import logging
from pydantic import BaseModel
import os
import json
from rq import Queue, Retry
from redis import Redis
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from lib.job_queue import get_job_status
from lib.gpt_scraper.websource import WebSource
from lib.api_clients import get_elasticsearch
from .seed_sources import seed
from contextlib import asynccontextmanager

from .routers import jvoy_api, koro_api, lib_api
from .globalState import GlobalState



logger = logging.getLogger(__name__)

redis = Redis(
    host=os.environ.get("REDIS_HOST", "sources_rq_redis.sources"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
)
job_queue = Queue(connection=redis, default_timeout=-1)

es_client = get_elasticsearch()


def setup_elasticsearch_indexes():
    """
    Creates any indexes not present on the connected elasticsearch database.
    Won't deeply merge or overwrite existing index/properties- only creates
    missing indeces.
    Config should match keyword args on:
    https://elasticsearch-py.readthedocs.io/en/v8.3.2/api.html#elasticsearch.client.IndicesClient.create
    """
    indices = {
        "datasources": {},
    }
    for idx, config in indices.items():
        if not es_client.indices.exists(index=idx):
            logger.info(f"Creating index {idx}")
            es_client.indices.create(index=idx, body=config)

    seed(es_client, "datasources")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code goes here
    app.state.global_state = GlobalState()
    setup_elasticsearch_indexes()
    yield
    # Shutdown code goes here

app = FastAPI(docs_url="/", lifespan=lifespan)

# Ensure static directory exists
if not os.path.exists("static"):
    os.makedirs("static")

# Mount static files server
app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(lib_api.router)
app.include_router(jvoy_api.router)
app.include_router(koro_api.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.exception_handler(exceptions.RequestValidationError)
# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request, exc):
#     logger.info(f"Request or Response validation failed!: {exc}")
#     exc_json = json.loads(exc.json())
#     return JSONResponse({"detail": exc_json}, status_code=422)


# @app.on_event("startup")
# async def startup_event() -> None:
#     setup_elasticsearch_indexes()


@app.get("/status")
def status(job_id: str):
    return get_job_status(job_id, redis)


class ScanArguments(BaseModel):
    uris: list[str]
    name: str

class SearchArguments(BaseModel):
    query: str

@app.post("/scan")
def gpt_scan_uri(payload: list[ScanArguments]):
    logger.info(f"Queueing scan fn, uris: {payload}")
    sources = [WebSource(source.name, source.uris) for source in payload]
    job = job_queue.enqueue_call(
        func="worker.jobs.scrape.scrape_sources",
        args=[sources],
        retry=Retry(max=3, interval=[10, 30, 60]),
    )

    # TODO instead of returning ID, maybe start stream and
    # poll here but stream to client as things are ready..

    return {"queued": True, "job_id": job.id}


def add_id(hit):
    return {**hit["_source"], "id": hit["_id"]}

def format_source(source_obj):
    return add_id(source_obj)


@app.get("/sources")
def list_sources():
    logger.info("Getting all registered sources")

    q = {"query": {"match_all": {}}}

    size = 20  # for now hardcoded

    try:
        results = es_client.search(index="datasources", body=q, scroll="2m", size=size)
    except Exception as e:
        logger.exception(e)
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
        "sources": [format_source(i) for i in results["hits"]["hits"]],
        "scroll_id": scroll_id,
    }


@app.post("/add-force-source")
async def add_source_from_payload(request: Request):
    """
    Escape hatch to register sources by pushing a known or manual-built json
    for the datasource instead of scanning the web portal.
    """
    json_req = await request.json()

    body = json.dumps(json_req)

    es_client.index(index="datasources", body=body)

    return {"success": True}


@app.post("/search")
def search_sources(payload: SearchArguments):
    logger.info(f"Searching sources with query: {payload.query}")

    q = {
        "query": {
            "multi_match": {
                "query": payload.query,
                "fields": ["name", "description", "tags", "uris", "source_type"]
            }
        }
    }

    try:
        results = es_client.search(index="datasources", body=q)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Error occurred while searching")

    formatted_results = [format_source(hit) for hit in results["hits"]["hits"]]

    return formatted_results