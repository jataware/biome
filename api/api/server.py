from fastapi import FastAPI
import logging
from pydantic import BaseModel
import os
from rq import Queue, Retry
from redis import Redis
from api.job_queue import get_job_status


logger = logging.getLogger(__name__)
app = FastAPI()

# TODO copy Dojo's setup that creates es indeces if missing?

redis = Redis(
    host=os.environ.get("REDIS_HOST", "sources_rq_redis.sources"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
)
job_queue = Queue(connection=redis, default_timeout=-1)


@app.get("/")
def index():
    logger.info("Get test route.")
    return {"hello": "sources is ready"}


@app.get("/status")
def status(job_id: str):
    return get_job_status(job_id, redis)


class ScanArguments(BaseModel):
    uris: list[str]
    name: str


@app.post("/scan")
def gpt_scan_uri(payload: ScanArguments):
    logger.info(f"Queueing scan fn, uris: {payload.uris}")

    job = job_queue.enqueue_call(
        func="workers.scan_uri_job.start",
        args=[payload.name, payload.uris[0]],
        retry=Retry(max=3, interval=[10, 30, 60]),
    )

    # TODO instead of returning ID, maybe start stream and
    # poll here but stream to client as things are ready..

    return {"queued": True, "job_id": job.id}
