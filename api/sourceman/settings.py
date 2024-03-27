from pydantic_settings import BaseSettings
import pprint

pp = pprint.PrettyPrinter(indent=2)


class Settings(BaseSettings):
    # EXTRACTOR_BATCH_SIZE: int = 2
    # AWS_BUCKET: str
    CACHE_DIR_NAME: str = "documents_cache"


settings = Settings()
print("Settings:")
pp.pprint(Settings().model_dump())
