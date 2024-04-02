from fastapi import FastAPI  # , HTTPException, status
import logging
from pydantic import BaseModel
from os import environ
from rq import Queue, Retry
from redis import Redis
from typing import Optional, List


logger = logging.getLogger(__name__)
app = FastAPI()
redis = Redis(
    environ.get("REDIS_HOST", "sourceman_rq_redis.sourceman"),
    environ.get("REDIS_PORT", "6379"),
)
q = Queue(connection=redis, default_timeout=-1)


@app.get("/")
def index():
    logger.info("Get test route.")
    return {"hello": "sourceman is ready"}


class ExtractArgs(BaseModel):
    uris: List[str]
    name: str

# TODO copy Dojo's setup that creates indeces if not existing


@app.post("/scan")
def gpt_scan_uri(payload: ExtractArgs):
    logger.info(f"Queueing scan fn, uris: {payload.uris}")

    job = q.enqueue_call(
        func="sourceman.scan_uri_job.start",
        args=[payload.name, payload.uris[0]],
        retry=Retry(max=3, interval=[10, 30, 60]),
    )

    # TODO instead of returning ID, maybe start stream and
    # poll here but stream to client as things are ready..

    return {"queued": True, "job_id": job.id}
