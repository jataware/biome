FROM --platform=linux/amd64 python:3.11.6-bookworm

WORKDIR /api
RUN apt update

RUN pip install --upgrade pip poetry
COPY ./pyproject.toml /api/

COPY ./README.md /api/README.md

RUN poetry install --no-root

# set display port to avoid crash. TODO Needed?
ENV DISPLAY=:99
