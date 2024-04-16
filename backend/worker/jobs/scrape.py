import logging
import json

from typing import Any
from lib.gpt_scraper.scraper import GPTScraper
from lib.gpt_scraper.websource import WebSource
from lib import api_clients


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def scrape_sources(sources: list[WebSource]):
    elastic = api_clients.get_elasticsearch()
    scraper = GPTScraper(api_clients.get_openai())
    for source in sources:
        source_details = scraper.scrape_web_source(source)
        # TODO hardcoded to 1st item... accepts multiple URIs
        # but we'll accept one for now, until we merge the
        # json output. Additionally, this may completely
        # change if doing a spider crawl from 1 URL
        body = json.dumps(source_details[0])
        elastic.index(index="datasources", body=body)
    return {}
