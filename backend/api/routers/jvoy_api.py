import subprocess
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from lib.models import JvoyTaskArguments
from typing import List
import hashlib
from datetime import datetime
from rq.job import Job
from markdown import markdown
import base64
from PIL import Image
from io import BytesIO
import re
import os

router = APIRouter(
    prefix="/jvoy",
    tags=["jvoy"],
    responses={404: {"description": "Not Found"}}
)

@router.post("/run_task")
def run_jvoy_task(
    payload: JvoyTaskArguments,
    request: Request
    ):

    # Create a string from the user task and the current date
    data = f'{payload.user_task}{datetime.now().isoformat()}'

    # Create a hash from the string
    job_id = hashlib.sha256(data.encode()).hexdigest()

    # Build the shell command
    # TODO: add support for the supporting docs--eg. coming from ES from the initial profiling
    # of the data source
    cmd = f'poetry run python -m jvoy.run -o "{payload.user_task}" -p "{payload.start_page}" -i "{job_id}"'
    
    job = request.app.state.global_state.job_queue.enqueue_call(
        func=subprocess.run,
        args=(cmd,),
        kwargs={'shell': True},
        job_id=job_id,
        meta={'job_timeout': 60},  # TTL in seconds
    )
    return {"queued": True, "job_id": job.id}

@router.get("/logs/{job_id}", response_model=List[str])
def get_logs(request: Request, job_id: str):
    # get redis connection
    r = request.app.state.global_state.redis

    # Get the logs from the 'logs' list in Redis
    logs = r.lrange(f'logs:{job_id}', 0, -1)

    # Convert the logs from bytes to strings
    logs = [log.decode('utf-8') for log in logs]

    # Invert the list
    # logs.reverse()

    # Remove elements that begin with "Element Labels" or "![log image"
    logs = [
        log for log in logs 
        if not log.startswith('Element Labels') 
        and not log.startswith('![log image')
    ]

    # Split the logs into chunks based on the "## Observation:" string
    # so each chunk is an observation and agent response
    chunks = []
    chunk = []
    for log in logs:
        if log.startswith('## Observation:'):
            if chunk:
                chunks.append(chunk)
            chunk = [log]
        else:
            chunk.append(log)
    if chunk:
        chunks.append(chunk)

    # Process markdown and base64 encoded images
    img_counter = 0
    for chunk in chunks:
        # added this image included checker to filter for just the first image
        # so that things are more readable in the UI
        # and the multiple JVoy scrolled screenshots are not included
        # image_included = False
        for i, log in enumerate(chunk):
            if log.startswith('base64 image:'):
                base64_str = log.replace('base64 image: ', '')
                img_data = base64.b64decode(base64_str)
                img = Image.open(BytesIO(img_data))
                img_path = f'static/images/{job_id}_{img_counter}.png'
                img_counter += 1

                # Ensure image directory exists
                if not os.path.exists("static/images"):
                    os.makedirs("static/images")

                img.save(img_path)
                chunk[i] = f'<img src="/api/{img_path}" style="width:40%; margin-bottom:2rem;"/>'
                # image_included = True
            elif log.startswith('base64 image:'):
                chunk[i] = ''  # Remove subsequent images from the chunk
            else:
                chunk[i] = markdown(log)

    # Convert each chunk to an HTML string
    chunks = ['\n'.join(chunk) for chunk in chunks]

    return chunks

@router.get("/kill/{job_id}")
def kill_job(request: Request, job_id: str):
    # get redis connection
    r = request.app.state.global_state.redis

    job = Job.fetch(job_id, connection=r)

    return job.kill()