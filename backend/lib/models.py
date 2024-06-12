from pydantic import BaseModel
from typing import Literal, List, Any


class ReplayStart(BaseModel):
    type: Literal["start"]
    url: str


class ReplayOption(BaseModel):
    text: str
    img: str


class ReplayParams(BaseModel):
    type: str
    options: dict[str, ReplayOption]
    selected: str
    name: str


class ReplayClickMetadata(BaseModel):
    attrs: dict[str, str | None]
    rect: dict[str, float]
    xpath: str


class ReplayElement(BaseModel):
    tag: str
    text: str


class ReplayClick(BaseModel):
    type: Literal["click"]
    url: str | None = None
    coordinate: list[int] | None = None
    element: ReplayElement
    eid: int | None = None
    img: str | None = None
    params: ReplayParams | None = None
    metadata: ReplayClickMetadata | None = None


class ReplayScroll(BaseModel):
    type: Literal["scroll"]
    scrollY: int


ReplayStep = ReplayStart | ReplayClick | ReplayScroll

# TODO: Adjust Replay model && transfer models to pacmens
class Replay(BaseModel):
    id: str
    action: str
    createdAt: int
    platform: str
    record: list[ReplayStep]


class JvoyQueryArguments(BaseModel):
    user_task: str
    supporting_docs: dict[str, Any] | None = None
    url: str = "https://www.google.com"


class JvoyPageanalyzerArguments(BaseModel):
    url: str


class WebSource(BaseModel):
    name: str
    uris: list[str]

