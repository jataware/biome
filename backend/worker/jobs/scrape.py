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
        body = json.dumps(source_details)
        elastic.index(index="datasources", body=body)
    return {}
