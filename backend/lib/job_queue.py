from datetime import datetime
from enum import Enum
from typing import Dict
from redis import Redis
from rq.exceptions import NoSuchJobError
from rq.job import Job
from fastapi import status
from pydantic import BaseModel
import subprocess


class Status(Enum):
    started = "started"
    finished = "finished"
    cancelled = "cancelled"
    complete = "complete"
    error = "error"
    queued = "queued"
    running = "running"
    failed = "failed"


class Result(BaseModel):
    created_at: datetime
    enqueued_at: datetime
    started_at: datetime | None
    job_result: Dict | None
    job_error: str | None


class SliceJob(BaseModel):
    id: str
    status: Status
    result: Result | None


def get_job_status(job_id: str, redis: Redis):
    try:
        job = Job.fetch(job_id, connection=redis)
        result = {
            "created_at": job.created_at,
            "enqueued_at": job.enqueued_at,
            "started_at": job.started_at,
            "job_error": job.exc_info,
            "job_result": {
            #     "args": job.return_value.args,
            #     "returncode": job.return_value.returncode,
            #     "stdout": job.return_value.stdout,
            #     "stderr": job.return_value.stderr,
            },
        }
        return SliceJob(id=job_id, status=job.get_status(), result=result)
    except NoSuchJobError:
        return status.HTTP_404_NOT_FOUND