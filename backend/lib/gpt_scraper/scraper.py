import json
from typing import Any
from openai import OpenAI
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from .schema import schema
from lib.gpt_scraper.websource import WebSource

# truncate to MAX_CHAR_LIMIT chars before passing to GPT
MAX_CHAR_LIMIT = 80000
# reject filtered pages under MINIMUM_PAGE_SIZE chars
MINIMUM_PAGE_SIZE = 10
# Feel free to change the model to gpt-3.5-turbo-1106
MODEL = "gpt-4-1106-preview"

MODEL_SYSTEM_CONTEXT = """
You are a master at scraping and parsing raw HTML. 
You will receive both the page url that hosted the data as well as the HTML content.
"""

PARSE_DATA_SPEC_TOOL = {
    "type": "function",
    "function": {
        "name": "parse_data",
        "description": "Parse raw HTML data nicely into json",
        "parameters": {
            "type": "object",
            "properties": {"data": {"type": "object", "properties": schema}},
        },
    },
}


class GPTScraper:
    client: OpenAI
    driver: webdriver.Firefox

    def __init__(self, client: OpenAI) -> None:
        self.client = client
        self.initialize_webdriver()

    def initialize_webdriver(self) -> None:
        options = FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def gpt_scrape_html(self, url: str, html_text: str) -> dict[str, Any]:
        completion = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": MODEL_SYSTEM_CONTEXT,
                },
                {"role": "user", "content": f"Page url: {url}"},
                {"role": "user", "content": html_text},
            ],
            tools=[PARSE_DATA_SPEC_TOOL],
            tool_choice={"type": "function", "function": {"name": "parse_data"}},
        )

        # Calling the data results
        tool_calls = completion.choices[0].message.tool_calls
        if tool_calls is None:
            raise Exception("returned openai tool calls returned no function usage")
        argument_dict = json.loads(tool_calls[0].function.arguments)
        return argument_dict["data"]

    def filter_html(self, html: str) -> str:
        """remove semantically irrelevant tags to shrink the html body size"""
        removal_regexes = [
            r"<head.*?>.*?</head>",
            r"<script.*?>.*?</script>",
            r"<style.*?>.*?</style>",
            r"<iframe.*?>.*?</iframe>",
            r'style=".*?>.*?"',
            r'class=".*?>.*?"',
        ]

        for regex in removal_regexes:
            html = re.sub(regex, "", html, flags=re.DOTALL)
        return html

    def scrape_page(self, target_url: str) -> dict[str, Any]:
        """
        uses selenium to fetch page contents with scripts included and ran
        before filtering the html and passing the rest to GPT
        """
        print(f"scraping single page: {target_url}")

        self.driver.get(target_url)
        self.driver.implicitly_wait(1.2)  # seconds

        # get raw html
        html_text = self.driver.page_source
        # Remove unnecessary part to prevent HUGE TOKEN cost!
        html_text = self.filter_html(html_text)
        filtered_size = len(html_text)

        print(f"\tpage size: {filtered_size}")
        if filtered_size < MINIMUM_PAGE_SIZE:
            print(f"\tpage size too small, discarding. body: '{html_text}'")
            return {}

        metadata_dict = self.gpt_scrape_html(target_url, html_text[:MAX_CHAR_LIMIT])
        metadata_dict["source_url"] = target_url
        return metadata_dict

    def scrape_web_source(self, source: WebSource) -> list[dict[str, Any]]:
        return [self.scrape_page(url) for url in source.uris]

    # TODO: should run in parallel!
    def scrape_web_sources(
        self, sources: list[WebSource], options={}
    ) -> dict[str, Any]:
        output = {source.name: self.scrape_web_source(source) for source in sources}
        return output
