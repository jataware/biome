# Datasource Browser

Codename: `Sources`

Web project to manage registering, browsing, tuning datasources.
- Frontend: Javascript with Nextjs / Reactjs
- Backend: python 3.11, `poetry` for dependency management and packaging.

## Requirements

- python 3.11
- poetry
- nodejs < 18.17
- docker, with compose plugin

## Initial Project Setup

1. Add environment variables to environment, or to `.env` file (for use with docker).
See file `env.sample` file for required variables. You may copy it for your own`.env`.

The variables with values on env.sample have a sensible default value. The rest are required (such as openai api key).

For the most part, during development, some values in `.env` can be picked up from
the HOST environment, so that's an option for sensitive data such as API keys,
which you may encrypt on disk.

## Quick Start

One the Initial project setup is completed,

Backend:
`docker compose --profile deploy --profile dev up -d`


The stack will start on port 8001.

UI on:

http://localhost:8001

Sample server request:

```
POST http://localhost:8001/api/scan
{
	"uris": ["https://my-datasource.gov"],
  "name": "My Datasource 101"
}
```

## Components

- FASTAPI Server (`api`)

A web server API to list, retrieve, register new datasources.

- Workers

Worker code for jobs related to scraping the web data portal / site to characterize
the types of data, formats, possible operations user wants to complete from this site
or even in combination with other sites.

- GUI (Datasource Management)

User interface to list/review datasources registered, as well as interact with
the web server API to register new datasources.

- elasticsearch 8.13

Currently used to store the scrape metatadata for each web portal source in JSON format.

- redis

Used to add queue (using redis queue) of jobs for workers to perform scraping and other operations


## Development

### RQ Tasks / Worker dashboard

Install `rq-dashboard` and run it (search pypi). You'll be able to navigate
to a web console and check that everything looks good, as well as inspect the
queued/running/failed jobs (web scraping, etc).

### Docker

When using docker, `server.py` and server files auto-reload and changes are available 
by sharing a mounted volume on our docker-cmopose setup. However, the rq tasks
worker process does not auto-reload: you'll either have to rebuild the image
or exec into container, and stop/re-start the rq process.

### Deploying

TODO
