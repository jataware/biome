"""
Jobs
"""
from enum import Enum
from redis import Redis
from rq import Queue, Retry
import rq.job as rq_job
from rq.exceptions import NoSuchJobError



from lib.settings import settings

### START FROM `job_queue.py`
class Result(BaseModel):
    created_at: datetime
    enqueued_at: datetime
    started_at: datetime | None
    job_result: Dict | None
    job_error: str | None


class SliceJob(BaseModel):
    id: str
    status: JobStatus
    result: Result | None


### END

# TODO: HOW DO I SPECIFY THE JOB INTERFACE
class JobType(Enum):
    SCAN = "worker.jobs.scan"
    QUERY = "worker.jobs.query"

class JobManager:
    """
    Starts long running, asynchronous jobs and handles their output.
    Jobs can optionally be given a session which is simply a collection 
    """

    def __init__(self):
        """
        Initializes queue and connection to Redis
            
        """
        self._redis = Redis(host=settings.REDIS_HOST)
        self._queue = Queue(connection=self._redis, default_timeout=-1)

    def init_session(self) -> str:
        """

        Returns
            str: The session id
        """
        raise NotImplemented
        

    def list_jobs(self, session_id: str) -> list[str]:
        """
        List all jobs associated with a given session
            
        Args:
            session_id (str): ID for the session to look up
        
        Returns
            list[str]: List of Job IDs for a given session
        """
        raise NotImplemented

    def exec(self):
        """
            
        """
        # ENQUEUE JOB
        # job = job_queue.enqueue_call(
        #     func="worker.jobs.scan",
        #     args=[sources],
        #     retry=Retry(max=3, interval=[10, 30, 60]),
        # )
        raise NotImplemented
        

    
    def write_message(self, job_id: str, message: str):
        """

        Args:
            job_id (str):
            message (str): Message to write to Job.

        """
        # logs = f"logs:{job_id}"
        # job_id = get_current_job().id
        raise NotImplemented

    def get_messages(self, job_id: str) -> list[str]:
        """
            
        Args:
            job_id (str): ID of job to read messages from.

        Returns:
            list[str]: Job Messages in insertion order
        """
        logs = redis.lrange(f'messages:{job_id}', 0, -1)
        return [log.decode('utf-8') for log in logs]
    

    def status(self, job_id: str) -> SliceJob | None:
        """
            
        """
        try:
            job = rq_job.Job.fetch(job_id, connection=self._redis)
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
            return

    def kill(self, job_id: str):
        """
        Kill job if it exists

        Args:
            job_id (str): ID of job to kill
        """
        job = rq_job.Job.fetch(job_id, connection=self._redis)
        job.kill()


