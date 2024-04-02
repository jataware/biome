from pydantic_settings import BaseSettings
import pprint

pp = pprint.PrettyPrinter(indent=2)

class Settings(BaseSettings):
    CACHE_DIR_NAME: str = "out"
    ELASTICSEARCH_URL: str = "localhost"
    ES_PORT: int = 9200

settings = Settings()
print("Settings:")
pp.pprint(Settings().model_dump())
