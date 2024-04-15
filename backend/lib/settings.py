from pydantic_settings import BaseSettings
import pprint

pp = pprint.PrettyPrinter(indent=2)

class Settings(BaseSettings):
    ELASTICSEARCH_URL: str = "http://localhost"
    ELASTICSEARCH_PORT: int = 9200
    OPENAI_API_KEY: str
    OPENAI_ORG_ID: str

settings = Settings()
pp.pprint(Settings().model_dump())
