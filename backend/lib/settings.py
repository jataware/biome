from pydantic_settings import BaseSettings
import pprint
import dotenv
from os import environ

pp = pprint.PrettyPrinter(indent=2)
dotenv.load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str = environ.get("OPENAI_API_KEY", "")
    OPENAI_ORG_ID: str = environ.get("OPENAI_ORG_ID", "")
    ES_USER: str | None  = environ.get("ES_USER", None)
    ES_PASS: str | None = environ.get("ES_PASS", None)
    ES_HOST: str | None = environ.get("ES_HOST", "http://localhost")
    ES_PORT: int | None = environ.get("ES_PORT", 9200)


settings = Settings()
