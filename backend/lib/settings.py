from pydantic_settings import BaseSettings
import pprint
import dotenv
import os

pp = pprint.PrettyPrinter(indent=2)
dotenv.load_dotenv()


class Settings(BaseSettings):
    ELASTICSEARCH_URL: str
    ELASTICSEARCH_PORT: int
    OPENAI_API_KEY: str
    OPENAI_ORG_ID: str


settings = Settings()
