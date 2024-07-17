from fastapi import FastAPI, exceptions, Request, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
import logging
from dataclasses import dataclass, asdict
import os
import json
import re
from typing import Any, Annotated
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from PIL import Image
from io import BytesIO
from markdown import markdown
import base64
import hashlib
from lib.settings import settings
from lib.sources_db import SourcesDatabase
from lib.job_runner import JobRunner, Operation

logger = logging.getLogger(__name__)

SourcesDB = Annotated[SourcesDatabase, Depends(SourcesDatabase)]
Runner = Annotated[JobRunner, Depends(JobRunner)]

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


##### JOBS #####

@dataclass
class ScanTarget:
    uris: list[str]
    name: str

@dataclass
class ScanArguments:
    targets: list[ScanTarget]
    session_id: str | None = None

    def __post_init__(self):
        if self.session_id is None:
            self.session_id = "default"


@app.post("/jobs/scan")
def scan_uri(payload: ScanArguments, runner: Runner):
    logger.info(f"Queueing scan fn, uris: {payload}")
    sources = [source.uris for source in payload.targets]
    job = runner.exec(
        operation=Operation.SCAN,
        args=[sources],
        session_id=payload.session_id,
    )
    return {"queued": True, "job_id": job.id}


@dataclass
class QueryArguments:
    user_task: str
    supporting_docs: dict[str, Any] | None = None
    url: str = "https://www.google.com"
    session_id: str | None = None

    def __post_init__(self):
        if self.session_id is None:
            self.session_id = "default"


@app.post("/jobs/query")
def query(payload: QueryArguments, runner: Runner):
    logger.info(f"Queueing query: {payload}")
    job = runner.exec(
        operation=Operation.QUERY,
        args={ k:v for (k,v) in asdict(payload).items() if k != "session_id" },
        session_id=payload.session_id,
    )
    
    return {"queued": True, "job_id": job.id}


@app.get("/jobs/{job_id}")
def status(job_id: str, runner: Runner):
    job = runner.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} does not exist.")
    return job


@app.delete("/jobs/{job_id}")
def kill_job(job_id: str, runner: Runner):
    return runner.kill_job(job_id)

# TODO(DESIGN): Come up with a better way to bubble up status
# We may want to rethink how progress is handled in the future
# as discussed in `/backend/worker/jobs.py`.
# TODO(DESIGN): Make this work for any task. Not just 'query'
@app.get("/jobs/{job_id}/logs", response_model=list[str])
def get_query_progress(job_id: str, runner: Runner):
    job = runner.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job does not exist.")
    
    logs = [
        log for log in job.messages 
        if not log.startswith('Element Labels') 
        and not log.startswith('![log image')
    ]

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

                #Check if the hash already exists in Redis
                # if not runner._redis.sismember(f'img_hashes:{job_id}', img_hash):
                if not os.path.exists(img_path):
                    # If the hash doesn't exist, save the image and add the hash to Redis
                    img = Image.open(BytesIO(img_data))

                    # Ensure image directory exists
                    if not os.path.exists("static/images"):
                        os.makedirs("static/images")

                    img.save(img_path)

                    # Add the hash to the 'img_hashes' set in Redis
                    # runner._redis.sadd(f'img_hashes:{job_id}', img_hash)

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


