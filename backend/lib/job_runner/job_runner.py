"""
Jobs
"""
from dataclasses import dataclass
from typing import Any
from uuid import uuid4
from enum import Enum
from datetime import datetime
from time import sleep
from redis import Redis
from rq import Queue, Retry, get_current_job
import rq.job as rq_job_lib
from rq.exceptions import NoSuchJobError

from lib.settings import settings

@dataclass
class Job:
    """
    Job contains its session, result (if it is complete),
    its status along with some metadata.

    This object represents the state of the Job on return.
    """
    id: str
    session_id: str
    status: rq_job_lib.JobStatus
    result: Any
    error: str | None
    messages: list[str]
    created_at: datetime
    enqueued_at: datetime
    started_at: datetime | None


class JobRunner:
    """
    Starts long running, asynchronous jobs and handles their output.
    Jobs can optionally be given a session which is simply a collection.
    """

    def __init__(self):
        """
        Initializes job queue and external connections.
        """
        self._redis = Redis(host=settings.REDIS_HOST)
        self._queue_name = 'default'


    def create_session(self) -> str:
        """
        Generate a new 'session' and return the ID to the user.

        A session is simply a collection of jobs.

        Returns
            str: ID of the newly created session
        """
        session_id = str(uuid4())        
        self._redis.rpush("sessions", session_id)
        return session_id


    @property
    def session_ids(self) -> list[str]:
        """
        List all sessions that currently exists.
            
        Returns
            list[str]: List of all session IDs.
        """
        session_ids = self._redis.lrange('sessions', 0, -1)
        return [session_id.decode('utf-8') for session_id in session_ids]


    def delete_session(self, session_id: str):
        """
        Delete session and associated jobs. 
        """
        job_ids = self.list_jobs(session_id)
        for job_id in job_ids:
            self._redis.delete(f"messages:{job_id}")
            self.delete_job(job_id)
        self._redis.delete(f"session:{session_id}")
        self._redis.lrem("session", session_id)


    def list_jobs(self, session_id: str) -> list[str]:
        """
        List all jobs associated with a given session.
            
        Args:
            session_id (str): ID for the session to look up.
        
        Returns
            list[str]: List of Job IDs for a given session.
        """

        if session_id not in self.session_ids:
            self._redis.rpush("sessions", session_id)
        job_ids = self._redis.lrange(f'sessions:{session_id}', 0, -1)
        return [job_id.decode('utf-8') for job_id in job_ids]


    def find_session(self, job_id: str) -> str | None:
        """
        Searches and returns the session for the given job ID.
        If the Job does not belong to a session, it is immediately
        deleted.
            
        Args:
            job_id (str): ID of Job to find session for.
        
        Returns:
            str | None: ID of the session if the job belongs to a session.
        """
        # While we are iterating through every session until we find a match.
        # we're not expecting the amount of sessions or jobs to be very high.
        # However, we could make this look up faster in exchange for more state
        # by storing a key `job:{job_id}:session` but this approach is adequate
        # for now. Storing the session_id as part of the job_id is another
        # option, but it complicates job retrieval a bit.
        for session_id in self.session_ids:
            if job_id in self.list_jobs(session_id):
                return session_id

        # A job without a session is an error state and should not exist.
        # TODO: Is this behaviour confusing for the client?
        self.kill_job(job_id)
        self.delete_job(job_id)


    def exec(self, operation: str, args: list | dict, session_id: str) -> str:
        """
        Kick off operation by creating a new job within the provided session.
            
        Args:
            operation (str): Path to function to run as job.
            args (list | dict): Arguments to pass to operation. Please look at the available 
                                args in `workers/jobs.py`.
            session_id (str): Session the created job belongs to.
            
        Returns:
            str: The newly created job ID
        """
        if session_id not in self.session_ids:
            self._redis.rpush("sessions", session_id)
        queue = Queue(self._queue_name, connection=self._redis, default_timeout=-1)        
        rq_job = queue.enqueue_call(
            func=operation,
            retry=Retry(max=3, interval=[10, 30, 60]),
            # Results are deleted when sessions are closed
            result_ttl=-1,
            # RQ allows for both kwargs and args to be passed in, however,
            # the `exec` interface only expects one group of arguments to
            # be passed in.
            **{('kwargs' if isinstance(args, dict) else 'args') : args}
        )
        self._redis.rpush(f"sessions:{session_id}", rq_job.id)
        return Job(
            id = rq_job.id,
            session_id = session_id,
            status = rq_job.get_status(),
            result = rq_job.return_value,
            error = rq_job.exc_info,
            messages = [],
            created_at = rq_job.created_at,
            enqueued_at = rq_job.enqueued_at,
            started_at = rq_job.started_at,
        )

    
    def write_message(self, job_id: str, message: str):
        """
        Write a message/log to the job. This is used to communicate
        with the client that started the job while the job is
        still running.

        Args:
            job_id (str):
            message (str): Message to write to Job.
        """
        messages_key = f"messages:{job_id}"
        self._redis.rpush(messages_key, message)


    def get_job(self, job_id: str | None = None) -> Job | None:
        """
        Get current state of the running job. ID defaults to the
        job the callee of this function is running in.
            
        Args:
            job_id (str | None): ID of Job to get status of. If no ID is 
                                 given, the caller will get the Job it
                                 is running in.

        Returns:
            Job | None: Current results of the Job if it exists
        """


        if job_id is not None:
            try:
                rq_job = rq_job_lib.Job.fetch(job_id, connection=self._redis)
            except NoSuchJobError:
                return
        else:
            rq_job = get_current_job()
            job_id = rq_job.id
           
        session_id = self.find_session(job_id)
        if session_id is None:
            return
        
        messages = [
            raw_msg.decode('utf-8')            
            for raw_msg in self._redis.lrange(f'messages:{job_id}', 0, -1)
        ]
        
        return Job(
            id = job_id,
            session_id = session_id,
            status = rq_job.get_status(),
            result = rq_job.return_value,
            error = rq_job.exc_info,
            messages = messages,
            created_at = rq_job.created_at,
            enqueued_at = rq_job.enqueued_at,
            started_at = rq_job.started_at,
        )


    def kill_job(self, job_id: str):
        """
        Kill job if it exists.

        Args:
            job_id (str): ID of job to kill
        """
        try:
            rq_job = rq_job_lib.Job.fetch(job_id, connection=self._redis)
        except NoSuchJobError:
            return
        else:
            rq_job.kill()


    def delete_job(self, job_id: str):
        """
        Delete job if it exists.

        Args:
            job_id (str): ID of job to delete
        """
        try:
            rq_job = rq_job_lib.Job.fetch(job_id, connection=self._redis)
        except NoSuchJobError:
            return
        else:
            rq_job.delete()


