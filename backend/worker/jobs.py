import logging
import json
from pathlib import Path


from jvoy.profiler import WebPageProfiler
from jvoy.driver import JvoyDriver

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


def query(url, supporting_docs, user_task, job_id):
    driver = JvoyDriver(
        url=url,
        supporting_docs=supporting_docs,
        results_dir=Path('/jvoy/results'),
        timeout=20,
        #adblock=False,
        #port=8080,
        job_id=job_id,
    )
    driver.run(user_task)
    driver.end()
    return {}
