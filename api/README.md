# Data Source Management

### Or: SOURCE MAN

## Initial Project Setup

1. Add environment variables to environment, or to .env file (for docker to use).
The following variables are supported:

```
CACHE_DIR_NAME="documents_cache"
```

The variables with values above share their default value. The rest are required.

## Running with docker

```
docker compose up -d
```

Server will start on port 8082. See [Deploying](#Deploying) if you'd like to also
start the router server which proxies from port 80.

Sample server request:

```
POST http://localhost:8082/scanner
{
	"uri": "https://my-datasource.gov"
}
```

Each processing returns a connecting to send back a message as updates occur.

## Development

### RQ Tasks / Worker dashboard

Install `rq-dashboard` and run it (search pypi). You'll be able to navigate
to a web console and check that everything looks good, as well as inspect the
queued/running/failed tasks.

### Docker

When using docker, `server.py` and server files auto-reload and changes are available 
by sharing a mounted volume on our docker-cmopose setup. However, the rq tasks
worker process does not auto-reload: you'll either have to rebuild the image
or exec into container, and stop/re-start the rq process.

### Deploying

To start the docker stack and a router server on port 80:
docker compose --profile deploy up -d
