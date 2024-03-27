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
# from sourceman.ocr import NougatExtractor


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    return Path(__file__).parent.parent


logger.info("Loaded scan_uri_job namespace")


CACHE_FOLDER = path_join(get_project_root(), settings.CACHE_DIR_NAME)
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)


def test_task(url):
    logger.info("\n===\nCounting words test task...")

    file1 = open("MyFileJobTest.txt", "w")
    L = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
    file1.writelines(L)
    file1.close()
    return len(url)


# extractor = NougatExtractor(batch_size=settings.EXTRACTOR_BATCH_SIZE)
# s3 = boto3.resource("s3")


def start(uri):
    """
    Uri example:
    https://datasource.gov/faq
    """

    logger.info(f"Starting uri scanning to json: {uri}")

    # BUCKET = settings.AWS_BUCKET

    cache_file_path = path_join(CACHE_FOLDER, f"{uri}.json")

    # s3_path = s3_url.replace(f"s3://{BUCKET}/", "")

    # try:
    #     if not os.path.isfile(cache_file_path):
    #         s3.Bucket(BUCKET).download_file(s3_path, cache_file_path)
    #     else:
    #         logger.info("File already cached, skip download.")
    # except botocore.exceptions.ClientError as e:
    #     logger.info("Failed S3 download.")
    #     raise e

    # text = extractor.extract_pdf_text(Path(cache_file_path))

    temp_file_path = None

    # with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
    #     f.write(text)
    #     temp_file_path = f.name

    # assert temp_file_path is not None, "temporary file should not be empty!"

    # os.remove(temp_file_path)

    # if callback_url:
    #     try:
    #         data = {
    #             "context": {
    #                 # "s3_key": s3_key,
    #                 "result": json_properties
    #             }
    #         }
    #         # requests.post(callback_url, data=json.dumps(data))
    #         # logger.info("Request successful to callback url.")
    #     except requests.RequestException as e:
    #         logger.error(f"Error making GET request to callback_url: {e}")
    #         raise e

    return f"====\nScanning and json data complete for: {uri}."


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
