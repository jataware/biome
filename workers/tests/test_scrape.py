import os
import os.path
import json
import dotenv

from openai import OpenAI
from workers.gpt_scraper.gpt_scraper import GPTScraper, WebSource

OUTPUT_DIR = os.path.join(".", "output")


def save_dict_to_json(data, filename: str):
    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=2))


WEB_SOURCES = [
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
    },
]

# Running program one by one:
# test_source = web_sources[0]
# test_name = test_source["name"]
# test_page = test_source["pages"][1]

# print("test_page:")
# print(test_page)
# print("running main")
# scrape_one_page(test_name, test_page, 1)
if __name__ == "__main__":
    dotenv.load_dotenv()
    print("running tests for web scraping")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    client = OpenAI(
        organization=os.environ.get("JATA_OPENAI_SCRAPE_ORG", ""),
        api_key=os.environ.get("JATA_OPENAI_SCRAPE_KEY", ""),
    )
    scraper = GPTScraper(client)
    scraped_text = scraper.scrape_multiple_pages(
        [WebSource(name=source["name"], pages=source["pages"]) for source in WEB_SOURCES]
    )
    save_dict_to_json(scraped_text, os.path.join(OUTPUT_DIR, "scrape_results.json"))
