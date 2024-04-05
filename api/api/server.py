import logging
import json
from pydantic import BaseModel
from os import environ
from rq import Queue, Retry
from redis import Redis
from typing import Optional, List
from .settings import settings

from elasticsearch import Elasticsearch

from fastapi import (
    FastAPI,
    File,
    HTTPException,
    Query,
    Response,
    UploadFile,
    status,
    Request,
    exceptions,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .seed_sources import seed


es = Elasticsearch(
    [
        {
            "scheme": "http",  # TODO env, or include with url var below
            "host": settings.ELASTICSEARCH_URL,
            "port": settings.ES_PORT,
        }
    ]
)


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
        if not es.indices.exists(index=idx):
            logger.info(f"Creating index {idx}")
            es.indices.create(index=idx, body=config)

    seed(es, "datasources")


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


def print_debug_routes() -> None:
    max_len = max(len(route.path) for route in app.routes)
    routes = sorted(
        [
            (method, route.path, route.name)
            for route in app.routes
            for method in route.methods
        ],
        key=lambda x: (x[1], x[0]),
    )
    route_table = "\n".join(
        f"{method:7} {path:{max_len}} {name}" for method, path, name in routes
    )
    logger.debug(f"Route Table:\n{route_table}")


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logger.info(f"Request or Response validation failed!: {exc}")
    exc_json = json.loads(exc.json())
    return JSONResponse({"detail": exc_json}, status_code=422)


@app.on_event("startup")
async def startup_event() -> None:
    setup_elasticsearch_indexes()
    # print_debug_routes()


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
    return {**hit["_source"], "id": hit["_id"]}


def format_source(source_obj):
    return add_id(source_obj)


@app.get("/sources")
def list_sources():
    logger.info("Getting all registered sources")

    q = {"query": {"match_all": {}}}

    size = 20  # for now hardcoded

    try:
        results = es.search(index="datasources", body=q, scroll="2m", size=size)
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

    es.index(index="datasources", body=body)

    return {"success": True}


class ExtractArgs(BaseModel):
    uris: List[str]
    name: str


@app.post("/scan")
def gpt_scan_uri(payload: ExtractArgs):
    """
    Queues scan of web portal given uris (although one for now).
    Name is required but only important for it to be unique for now.. (a bit useless; remove)
    """
    logger.info(f"Queueing scan fn, uris: {payload.uris}")

    job = q.enqueue_call(
        func="workers.scan_uri_job.start",
        args=[payload.name, payload.uris[0]],
        retry=Retry(max=3, interval=[10, 30, 60]),
    )

    # TODO instead of returning ID, maybe start stream and
    # poll here but stream to client as things are ready..

    return {"queued": True, "job_id": job.id}
