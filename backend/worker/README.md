
The `gpt_scraper` namespace contains logic to start a headless firefox browser
and pass the clean HTML to gpt4 using function calling, to get the data back
following a given expected schema.

Schema file [here](workers/gpt_scraper/scrape_schema.py)

Guide to `openai` funtion calling:

https://platform.openai.com/docs/guides/function-calling
