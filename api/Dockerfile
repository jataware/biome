FROM --platform=linux/amd64 python:3.11.6-bookworm

WORKDIR /sourceman

RUN apt update
RUN pip install --upgrade pip poetry
COPY ./pyproject.toml /sourceman/
RUN poetry install --no-root

COPY ./README.md /sourceman/README.md

RUN poetry install
