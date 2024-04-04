import logging
import json
from workers.gpt_scraper.gpt_scraper import GPTScraper, WebSource
from workers import api_clients


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
