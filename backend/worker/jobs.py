import logging
import json
from pathlib import Path
from base64 import b64encode

from rq import get_current_job
from jvoy.profiler import WebPageProfiler
from jvoy.driver import JvoyDriver
from jvoy.record import RecordType, ActionRecord, ScreenshotRecord

from lib import api_clients
from lib.settings import Settings


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

def scan(sources: list[list[str]]):
    elastic = api_clients.get_elasticsearch()
    for uris in sources:
        # TODO hardcoded to 1st item... accepts multiple URIs
        # but we'll accept one for now, until we merge the
        # json output. Additionally, this may completely
        # change if doing a spider crawl from 1 URL
        profiler = WebPageProfiler(uris[0], "dump")
        results = profiler.run()
        body = json.dumps(results)
        elastic.index(index="datasources", body=body)
    return {}


def query(url, supporting_docs, user_task):
    ##### Callback #####
    # TODO: Log messages to a service that's not Redis and not Markdown
    # This current logic was copy-pasted from jvoy with very little
    # modification. We should consider a more robust logging solution
    # in the long term. We are currently generated markdown and writing
    # it to Redis. Then, the markdown is read from Redis and compiled
    # HTML. Instead, we should just pass data and let the UI decide
    # how to render it.
    job_id = get_current_job().id
    redis = Redis(
        host=Settings.REDIS_HOST,
    )
    logs = f"logs:{job_id}"

    def report(record: RecordType):
        match record:
            case ActionRecord(title, text):
                if "Element Labels" in title:
                    return
                message = f'## {title}\n{text}\n\n'
                message = message.replace('<', '&lt;').replace('>', '&gt;')
                message += "\n\n"
                redis.rpush(logs, message)
            case ScreenshotRecord(data, ext):
                encoded_image = b64encode(data).decode('utf-8')
                redis.rpush(logs, f'base64 image: {encoded_image}\n\n')
            # Ignore remaining record types
            case _:
                pass


    ##### Job #####
    driver = JvoyDriver(
        url=url,
        supporting_docs=supporting_docs,
        results_dir=Path('/jvoy/results'),
        timeout=20,
        #adblock=False,
        #port=8080,
        record_callback=report,
    )
    answer = driver.run(user_task)
    report(ActionRecord("Answer", answer))
    import time
    time.sleep(6)
    driver.end()
    return {}
