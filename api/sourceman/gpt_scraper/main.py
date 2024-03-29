import json
import requests
from openai import OpenAI
import re
import pprint
import argparse
from pathlib import Path
from os.path import join as path_join, exists as path_exists
from os import getenv, makedirs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv
from .scrape_schema import schema, simple_schema


load_dotenv()  # use .env
pp = pprint.PrettyPrinter(indent=2)


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def output_path(filename):
    return path_join(get_project_root(), "out", filename)


out_dir = path_join(get_project_root(), "out")

if not path_exists(out_dir):
    print("Creating out dir")
    makedirs(out_dir)


# Mock, tests
web_sources = [
    {
        "name": "Genomic Data Commons",
        "pages": [
            "https://gdc.cancer.gov/about-gdc/gdc-faqs",
            "https://gdc.cancer.gov/support/gdc-webinars",
        ],
    },
    {
        "name": "Proteomic Data Commons",
        "pages": [
            "https://pdc.cancer.gov/pdc/about",
            "https://pdc.cancer.gov/pdc/data-use-guidelines",
            "https://pdc.cancer.gov/pdc/data-dictionary",
        ],
    },
    {
        # Clinical and Translational Data Commons
        "name": "Clinical and Translational Data Commons",
        "pages": [
            "https://datacommons.cancer.gov/repository/clinical-and-translational-data-commons",
            "https://moonshotbiobank.cancer.gov/",
        ],
    },
    {
        "name": "Imaging Data Commons",
        "pages": [
            # "https://portal.imaging.datacommons.cancer.gov/"
            "https://learn.canceridc.dev/"
            "https://learn.canceridc.dev/getting-started-with-idc",
            "https://learn.canceridc.dev/core-functions-of-idc",
            "https://learn.canceridc.dev/data/introduction",
            "https://learn.canceridc.dev/frequently-asked-questions",
            "https://learn.canceridc.dev/support",
        ],
    },
    {
        "name": "Cancer Research Data Commons",
        "pages": [
            "https://datacommons.cancer.gov/explore",
            "https://datacommons.cancer.gov/support-for-researchers",
            "https://datacommons.cancer.gov/publications",
            "https://datacommons.cancer.gov/about",
            "https://datacommons.cancer.gov/explore/select-datasets",
            "https://datacommons.cancer.gov/crdc-faqs",
        ],
    },
    {
        "name": "Cancer Data Service",
        "pages": [
            "https://datacommons.cancer.gov/repository/cancer-data-service",
            "https://dataservice.datacommons.cancer.gov/#/home",
            "https://dataservice.datacommons.cancer.gov/#/programs",
            "https://dataservice.datacommons.cancer.gov/#/studies",
            "https://dataservice.datacommons.cancer.gov/#/cancerDataService",
        ],
    },
    {
        "name": "Seven Bridges Cancer Genomics Cloud",
        "pages": [
            "https://docs.cancergenomicscloud.org/docs/before-you-start",
            "https://docs.cancergenomicscloud.org/page/uncontrolled-data-quickstart-guide",
            "https://docs.cancergenomicscloud.org/docs/about-datasets",
        ],
    },
    {
        "name": "ISB Cancer Gateway in the Cloud",
        "pages": [
            "https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/HowToGetStartedonISB-CGC.html",
            "https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/FAQ.html",
            "https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/ExploringISB-CGC.html",
        ],
    }
]


print("web_sources:")
print(web_sources)


client = OpenAI(
    organization=getenv("JATA_OPENAI_SCRAPE_ORG"),
    api_key=getenv("JATA_OPENAI_SCRAPE_KEY"),
)

parse_data_spec = {
    "type": "function",
    "function": {
        "name": "parse_data",
        "description": "Parse raw HTML data nicely into json",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object", "properties": schema
                }
            },
        },
    },
}

print("parse data spec:")
pp.pprint(parse_data_spec)


def gpt_scrape_html(html_text):
    # Chat Completion API from OpenAI
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",  # Feel free to change the model to gpt-3.5-turbo-1106
        messages=[
            {
                "role": "system",
                "content": "You are a master at scraping and parsing raw HTML.",
            },
            {"role": "user", "content": html_text},
        ],
        tools=[parse_data_spec],
        tool_choice={"type": "function", "function": {"name": "parse_data"}},
    )

    # Calling the data results
    argument_str = (
        completion.choices[0].message.tool_calls[0].function.arguments
    )
    argument_dict = json.loads(argument_str)
    return argument_dict["data"]


def truncate_string(input_string, max_length):
    """
    Trims a string to the specified character count.
    """
    if len(input_string) <= max_length:
        return input_string
    else:
        return input_string[:max_length]


def scrape_one_page(name, target_url, page_index):
    print(f"Scraping {target_url}")

    save_filename = output_path(
        name.replace(" ", "_") + "_" + str(page_index) + ".json"
    )

    print("filename:")
    print(save_filename)

    # TODO decide what to do with repeated requests, as names aren't required to
    # be unique. This is mostly only needed for demo purposes
    if path_exists(save_filename):
        print("File already exists, skipping...")
        return

    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    driver.get(target_url)
    driver.implicitly_wait(1.2)  # seconds

    # get raw html
    html_text = driver.page_source

    # Remove unnecessary part to prevent HUGE TOKEN cost!
    # Remove everything between <head> and </head>
    html_text = re.sub(r"<head.*?>.*?</head>", "", html_text, flags=re.DOTALL)
    # Remove all occurrences of content between <script> and </script>
    html_text = re.sub(
        r"<script.*?>.*?</script>", "", html_text, flags=re.DOTALL
    )
    # Remove all occurrences of content between <style> and </style>
    html_text = re.sub(r"<style.*?>.*?</style>", "", html_text, flags=re.DOTALL)
    html_text = re.sub(
        r"<iframe.*?>.*?</iframe>", "", html_text, flags=re.DOTALL
    )
    html_text = re.sub(r'style=".*?>.*?"', "", html_text, flags=re.DOTALL)
    html_text = re.sub(r'class=".*?>.*?"', "", html_text, flags=re.DOTALL)

    # NOTE If we need to save the scraped HTML for debugging/etc:
    # with open(output_path(save_filename.replace("json", "html")), "w") as ff:
    #     ff.write(html_text)

    print("\n=======\nHTML LEN:")
    print(len(html_text))

    if len(html_text) > 10:
        metadata_dict = gpt_scrape_html(truncate_string(html_text, 80000))
    else:
        print("html len is too short, not proceeding")
        print(html_text)
        print("FAILED")
        return {}

    with open(save_filename, "w") as f:
        f.write(json.dumps(metadata_dict, indent=2))

    return metadata_dict


# TODO for running locally/main/demo with hardcoded websources
def scrape_all_pages():
    for source_index, source_obj in enumerate(web_sources):
        for page_index, page in enumerate(web_sources[source_index]["pages"]):
            name = source_obj["name"]
            scrape_one_page(name, page, page_index)


if __name__ == "__main__":
    scrape_all_pages()
    # Running program one by one:
    # test_source = web_sources[0]
    # test_name = test_source["name"]
    # test_page = test_source["pages"][1]

    # print("test_page:")
    # print(test_page)
    # print("running main")
    # scrape_one_page(test_name, test_page, 1)
