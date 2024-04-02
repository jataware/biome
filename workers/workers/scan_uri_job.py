import os
import logging
import json
from pathlib import Path
from os.path import join as path_join
import tempfile
import requests
from elasticsearch import Elasticsearch

from workers.settings import settings
from workers.gpt_scraper.main import scrape_one_page


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

es = Elasticsearch(
    [
        {
            "scheme": "http", # TODO env, or include with url var below
            "host": settings.ELASTICSEARCH_URL,
            "port": settings.ES_PORT,
        }
    ]
)


def get_project_root() -> Path:
    return Path(__file__).parent.parent



# CACHE_FOLDER = path_join(get_project_root(), settings.CACHE_DIR_NAME)
# if not os.path.exists(CACHE_FOLDER):
#     os.makedirs(CACHE_FOLDER)


def test_task(url):
    logger.info("\n===\nCounting words test task...")

    file1 = open("MyFileJobTest.txt", "w")
    L = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
    file1.writelines(L)
    file1.close()
    return len(url)




def start(name, uri, index=0):
    """
    Uri example:
    https://datasource.gov/faq
    """

    logger.info(f"Starting uri scanning to json: {uri}")

    result = scrape_one_page(name, uri, index)

    result["metadata"] = {
        # TODO
        # "created_at": 0,
        # "updated_at": 0,
        "scanned_uris": [uri] # Only works for 1st scrape on base site
    }

    body = json.dumps(result)
    es.index(index="datasources", body=body)

    # TODO return results in server-push stream?

    return result




# if __name__ == "__main__":
    # import sys

    # root = logging.getLogger()
    # root.setLevel(logging.DEBUG)

    # handler = logging.StreamHandler(sys.stdout)
    # handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    # )
    # handler.setFormatter(formatter)
    # root.addHandler(handler)

    # logger.info("Running main file")
