from fastapi import FastAPI, exceptions, Request, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
import logging
from dataclasses import dataclass, asdict
import os
import json
import re
from typing import Any, Annotated
from datetime import datetime
from rq import Queue, Retry
from rq.job import Job
from redis import Redis
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from PIL import Image
from io import BytesIO
from markdown import markdown
import base64
import hashlib
from lib.job_queue import get_job_status
from lib.settings import settings
from lib.sources_db import SourcesDatabase

logger = logging.getLogger(__name__)

redis = Redis(
    host=settings.REDIS_HOST,
)
job_queue = Queue(connection=redis, default_timeout=-1)

SourcesDB = Annotated[SourcesDatabase, Depends(SourcesDatabase)]

app = FastAPI(docs_url="/")

# Ensure static directory exists
if not os.path.exists("static"):
    os.makedirs("static")

# Mount static files server
app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##### SOURCES #####

# TODO: Enable scrolling
@app.get("/sources")
def search_sources(db: SourcesDB, query: str | None = None):
    if query is None:
        logger.info("Getting all registered sources")
    else:
        logger.info(f"Searching sources with query: {query}")
    result = db.search(query)
    return {
        "total": result.total,
        "sources": result.sources,
    }


@app.post("/sources")
async def add_source_from_payload(request: Request, db: SourcesDB):
    """
    Escape hatch to register sources by pushing a known or manual-built json
    for the datasource instead of scanning the web portal.
    """
    json_req = await request.json()
    db.store(json_req)
    return {"success": True}


##### TASKS #####

@dataclass
class ScanArguments:
    uris: list[str]
    name: str


@app.post("/tasks/scan")
def scan_uri(payload: list[ScanArguments]):
    logger.info(f"Queueing scan fn, uris: {payload}")
    sources = [source.uris for source in payload]
    job = job_queue.enqueue_call(
        func="worker.jobs.scan",
        args=[sources],
        retry=Retry(max=3, interval=[10, 30, 60]),
    )
    return {"queued": True, "job_id": job.id}

@dataclass
class QueryArguments:
    user_task: str
    supporting_docs: dict[str, Any] | None = None
    url: str = "https://www.google.com"

@app.post("/tasks/query")
def query(payload: QueryArguments):
    logger.info(f"Queueing query: {payload}")
    job = job_queue.enqueue_call(
        func="worker.jobs.query",
        kwargs=asdict(payload),
        retry=Retry(max=3, interval=[10, 30, 60]),
    )
    return {"queued": True, "job_id": job.id}

@app.get("/tasks/{job_id}")
def status(job_id: str):
    return get_job_status(job_id, redis)

@app.delete("/tasks/{job_id}")
def kill_job(job_id: str):
    job = Job.fetch(job_id, connection=redis)
    return job.kill()

# TODO: Come up with a better way to bubble up status
# We may want to rethink how progress is handled in the future
# as discussed in `/backend/worker/jobs.py`.
# TODO: Make this work for any task. Not just 'query'
@app.get("/tasks/{job_id}/logs", response_model=list[str])
def get_query_progress(job_id: str):
    logs = redis.lrange(f'logs:{job_id}', 0, -1)

    logs = [log.decode('utf-8') for log in logs]
    
    logs = [
        log for log in logs 
        if not log.startswith('Element Labels') 
        and not log.startswith('![log image')
    ]

    # logs.reverse()

    chunks = []
    chunk = []
    for log in logs:
        if log.startswith('## Observation'):
            if chunk:
                chunks.append(chunk)
            chunk = [log]
        else:
            chunk.append(log)
    if chunk:
        chunks.append(chunk)

    for chunk in chunks:
        image_added = False
        for i, log in enumerate(chunk):
            if log.startswith('base64 image:') and not image_added:
                base64_str = log.replace('base64 image: ', '')
                img_data = base64.b64decode(base64_str)

                # Create a hash of the image data
                img_hash = hashlib.sha256(img_data).hexdigest()
                img_path = f'static/images/{job_id}_{img_hash}.png'

                # Check if the hash already exists in Redis
                if not redis.sismember(f'img_hashes:{job_id}', img_hash):
                    # If the hash doesn't exist, save the image and add the hash to Redis
                    img = Image.open(BytesIO(img_data))

                    # Ensure image directory exists
                    if not os.path.exists("static/images"):
                        os.makedirs("static/images")

                    img.save(img_path)

                    # Add the hash to the 'img_hashes' set in Redis
                    redis.sadd(f'img_hashes:{job_id}', img_hash)

                # even if the image is already saved, we still need to update the log chunk with the image tag
                chunk[i] = f'<a href="/api/{img_path}" target="_blank"><img src="/api/{img_path}"/></a>'
                image_added = True
            elif log.startswith('base64 image:'):
                chunk[i] = '' 
            else:
                # this is a regular (text) log entry
                # Make 'Action:' and 'Thought:' bold, etc
                log = log.replace('ANSWER;', '<b>ANSWER:</b>')
                log = log.replace('Action:', '<b>Action:</b>')
                log = log.replace('Thought:', '<b>Thought:</b>')
                log = log.replace('State:', '<b>Action:</b>')
                log = log.replace('Plan:', '<b>Thought:</b>')

                # Find URLs and replace them with <a> tags
                url_pattern = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
                log = re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', log)

                chunk[i] = markdown(log)

    # Convert each chunk to an HTML string
    chunks = ['\n'.join(chunk) for chunk in chunks]

    return chunks


