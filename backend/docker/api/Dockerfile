FROM --platform=linux/amd64 python:3.11.6-bookworm

WORKDIR /backend
RUN apt update

RUN pip install --upgrade pip poetry
COPY ./pyproject.toml /backend/

COPY ./README.md /backend/README.md

RUN poetry install --no-root

# set display port to avoid crash. TODO Needed?
ENV DISPLAY=:99
