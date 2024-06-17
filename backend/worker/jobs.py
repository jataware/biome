import logging
import json
from pathlib import Path
from base64 import b64encode

from rq import get_current_job
from jvoy.profiler import WebPageProfiler
from jvoy.driver import JvoyDriver, LogAction
from jvoy.log import LogType

from lib import api_clients


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
    # TODO: Log messages to a service that's not Redis
    # This current logic was copy-pasted from jvoy with very little
    # modification. We should consider a more robust logging solution
    # in the long term.
    job_id = get_current_job().id
    redis = api_clients.get_redis()
    logs = f"logs:{job_id}"
    

    def callback(action: LogAction):
        log, log_type = action.data, action.log_type

        logger.error(f"\n\n{log_type} - {redis.lrange(f'logs:{job_id}', 0, -1)}\n\n")

        def write_message(log):
            logger.error("write message")
            redis.rpush(logs, log)

        def write_image(log):
            logger.error("write image")
            encoded_image = b64encode(log).decode('utf-8')
            redis.rpush(logs, f'base64 image: {encoded_image}\n\n')
        
        def write_undefined(log):
            logger.error(f"Unknown log type: {log_type}")

        log_type_map = {
            LogType.MESSAGE : write_message,
            LogType.IMAGE : write_image,
        }

        log_type_map.get(log_type, write_undefined)(log)


    ##### Job #####
    driver = JvoyDriver(
        url=url,
        supporting_docs=supporting_docs,
        results_dir=Path('/jvoy/results'),
        timeout=20,
        #adblock=False,
        #port=8080,
        logger_callback=callback,
    )
    driver.run(user_task)
    driver.end()
    return {}
