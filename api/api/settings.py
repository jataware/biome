from pydantic_settings import BaseSettings
import pprint
import dotenv
import os

pp = pprint.PrettyPrinter(indent=2)
dotenv.load_dotenv()


class Settings(BaseSettings):
    ELASTICSEARCH_URL: str = os.environ.get("ELASTICSEARCH_URL", "")
    ELASTICSEARCH_PORT: int = int(os.environ.get("ELASTICSEARCH_PORT", 9200))


settings = Settings()
