from dataclasses import dataclass


@dataclass
class WebSource:
    name: str
    uris: list[str]
