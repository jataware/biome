import os
import logging
import boto3
import json
import botocore.exceptions
from pathlib import Path
from os.path import join as path_join
import tempfile
import requests

from sourceman.settings import settings
from sourceman.gpt_scraper.main import scrape_one_page

# from sourceman.ocr import NougatExtractor


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    return Path(__file__).parent.parent


logger.info("Loaded scan_uri_job namespace")


CACHE_FOLDER = path_join(get_project_root(), settings.CACHE_DIR_NAME)
# if not os.path.exists(CACHE_FOLDER):
#     os.makedirs(CACHE_FOLDER)


def test_task(url):
    logger.info("\n===\nCounting words test task...")

    file1 = open("MyFileJobTest.txt", "w")
    L = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
    file1.writelines(L)
    file1.close()
    return len(url)


# extractor = NougatExtractor(batch_size=settings.EXTRACTOR_BATCH_SIZE)
# s3 = boto3.resource("s3")


def start(name, uri, index=0):
    """
    Uri example:
    https://datasource.gov/faq
    """

    logger.info(f"Starting uri scanning to json: {uri}")

    # cache_file_path = path_join(CACHE_FOLDER, f"{uri}.json")

    result = scrape_one_page(name, uri, index)

    print(f"====\nScanning and json data complete for: {uri}.")

    # TODO actually return something to stream as steps are completed

    return result


def tryit():
    mock_job_id = "3ff8aa9a-32bb-49fa-be94-6718e40cbd22_paragraph_embeddings_processors.calculate_store_embeddings"
    mock_url = "http://192.168.1.253:8000/job/3ff8aa9a-32bb-49fa-be94-6718e40cbd22/paragraph_embeddings_processors.calculate_store_embeddings"
    # mock_key = "3ff8aa9a-32bb-49fa-be94-6718e40cbd22-DIDX-documents/125284.mmd"

    res = requests.post(mock_url, data=json.dumps({
        "context": {
            "s3_key": mock_key,
            "document_id": "3ff8aa9a-32bb-49fa-be94-6718e40cbd22"
        }
    }))

    logger.info(f"got status code: {res.status_code}")


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

    # MOCK_ID = "fb18f69c-bd3e-4a44-91ab"
    # MOCK_URL = "s3://fb18f69c-bd3e-4a44-91ab/hello.pdf"

    # extract_text_from_S3_doc(MOCK_ID, MOCK_URL)
