from fastapi import APIRouter, Request

from lib.browser_pool import active_clients
from lib.job_queue import get_job_status

router = APIRouter(
    prefix="/lib",
    tags=["lib"],
    responses={404: {"description": "Not Found"}}
)

@router.get("/displays")
def displays():
    return active_clients()

@router.get("/status")
def status(
    job_id: str,
    request: Request
    ):
    return {"job": get_job_status(job_id, request.app.state.global_state.redis)}