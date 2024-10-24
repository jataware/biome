# Biome 

Biome is an AI powered platform for performing the next generation of biomedical research. It is currently in the prototype stage of development and is under active development.

The goal of Biome is to seamlessly combine the ability to find research data with an ability to deeply analyze it--all from the same user interface. To accomplish this, Biome provides users both a chat and notebook style interface with specialized AI integrations under the hood that enable sophisticated interactions with a variety of biomedical data sources as well as domain specific software libraries and tools. 

Biome is being developed under ARPA-H's [Biomedical Data Fabric (BDF) Toolbox](https://arpa-h.gov/news-and-events/arpa-h-announces-effort-develop-single-data-system-biomedical-research) program.

## Requirements

- docker-compose

## Getting started 

Many environment variables will need to be defined. See `env.sample` for one to copy and paste, and/or consult the same thing inline below.

You will need to add the API keys.

```
# API Keys
OPENAI_API_KEY=<your API key>
GEMINI_API_KEY=<your API key>

#
# Deployment Specific 
# -- only change below this line if you have special requirements for environment!
#

# Jupyter
JUPYTER_SERVER=http://jupyter:8888
JUPYTER_TOKEN=89f73481102c46c0bc13b2998f9a4fce
PYTHONPATH=/jupyter
ENABLE_CHECKPOINTS=true
TOOL_ENABLED_ASK_USER=true
TOOL_ENABLED_RUN_CODE=true

# Elasticsearch
ES_HOST="biome_es.biome"
ES_PORT=9200
STACK_VERSION=8.13.0
CLUSTER_NAME=biome-es-cluster
# Increase or decrease based on the available host memory (in bytes)
ES_MEM_LIMIT=1073741824  # 1GB
KB_MEM_LIMIT=1073741824  # 1GB
LICENSE=basic
KIBANA_PORT=5601
```

After that, run `docker-compose build --no-cache`.

### Initialization

Starting the project with the following command: 
```
docker compose up -d
```

and can be brought down with
```
docker compose down
```

## Usage

Visit http://localhost:8080/chat in the browser to use the chat interface.

Visit http://localhost:8080/notebook to use the notebook interface.

Both can be toggled within the UI itself as well, with persistent sessions.

### Development

#### Docker

`docker compose build` or `docker compose up --build` are usually sufficient
for rebuilding containers when their dependencies have been updated,
but use `docker compose build --no-cache` if you want to force everything to rebuild.
If a container doesn't have hot-reloading, it's usually enough to just the container
down and up again to have the changes reflected.

## Architecture

### Services 

- Biome UI (8080): Notebook and chat support through Beaker
