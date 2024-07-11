from datetime import datetime
from enum import Enum
from typing import Dict
from redis import Redis
from rq.exceptions import NoSuchJobError
from rq.job import Job, JobStatus
from fastapi import status
from pydantic import BaseModel


class Result(BaseModel):
    created_at: datetime
    enqueued_at: datetime
    started_at: datetime | None
    job_result: Dict | None
    job_error: str | None


class SliceJob(BaseModel):
    id: str
    status: JobStatus
    result: Result


def get_job_status(job_id: str, redis: Redis):
    try:
        job = Job.fetch(job_id, connection=redis)
        status = job.get_status()        
        result = {
            "created_at": job.created_at,
            "enqueued_at": job.enqueued_at,
            "started_at": job.started_at,
            "job_error": job.exc_info,
            "job_result": None if status != "finished" else job.return_value,
        }
        return SliceJob(id=job_id, status=status, result=result)
    except NoSuchJobError:
        return status.HTTP_404_NOT_FOUND
