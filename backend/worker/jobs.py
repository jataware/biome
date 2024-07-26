import logging
import json
from pathlib import Path
from base64 import b64encode
import shutil

from redis import Redis
from rq import get_current_job
from jvoy.profiler import WebPageProfiler
from jvoy.driver import JvoyDriver
from jvoy.record import RecordType, ActionRecord, ScreenshotRecord

from lib.sources_db import SourcesDatabase
from lib.job_runner import JobRunner, Job
from lib.settings import settings


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

def scan(sources: list[list[str]]):
    db = SourcesDatabase()
    for uris in sources:
        # TODO hardcoded to 1st item... accepts multiple URIs
        # but we'll accept one for now, until we merge the
        # json output. Additionally, this may completely
        # change if doing a spider crawl from 1 URL
        profiler = WebPageProfiler(uris[0], "dump")
        results = profiler.run()
        db.store(results)
    return {}


def query(url, supporting_docs, user_task):
    # TODO: Remove hack when jvoy is fixed to return answer 
    # JVOY doesn't return the final answer so we have to get it out of the callback
    final_answer = None

    ##### Callback #####
    # TODO: Log messages to a service that's not Redis and not Markdown
    # This current logic was copy-pasted from jvoy with very little
    # modification. We should consider a more robust logging solution
    # in the long term. We are currently generated markdown and writing
    # it to Redis. Then, the markdown is read from Redis and compiled
    # HTML. Instead, we should just pass data and let the UI decide
    # how to render it.
    runner =JobRunner()
    job_id = runner.get_job().id

    def report(record: RecordType):
        match record:
            case ActionRecord(title, text):
                if "Element Labels" in title or "Read Page" in title:
                    return
                # NOTE: See `final_answer` comments. This case should eventually be removed
                if "Answer" in title:
                    nonlocal final_answer
                    final_answer = text
                message = f'## {title}\n{text}\n\n'
                message = message.replace('<', '&lt;').replace('>', '&gt;')
                message += "\n\n"
                runner.write_message(job_id, message)
            case ScreenshotRecord(data, ext):
                encoded_image = b64encode(data).decode('utf-8')
                runner.write_message(job_id, f'base64 image: {encoded_image}\n\n')
            # Ignore remaining record types
            case _:
                pass


    ##### Job #####
    driver = JvoyDriver(
        url=url,
        supporting_docs=supporting_docs,
        results_dir=Path('/results'),
        timeout=20,
        adblock=False,
        port=8080, 
        record_callback=report,
    )
    driver.run(user_task)

    # TODO: Remove this hack
    # We have to make sure not to end the job so that the UI will listen
    # for the last message. Once UI rendering of queries is over, this 
    # should no longer be necessary.
    import time
    time.sleep(6)

    driver.end()

    for path in driver.download_tracker.get_all_downloads():
        shutil.move(path, "/results")
    shutil.rmtree(str(driver.download_tracker.downloads_dir))

    assert final_answer is not None, "Final answer not found"
    return {
        "answer": final_answer,
    }
