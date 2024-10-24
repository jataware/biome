# Biome 

Biome is an AI powered platform for performing the next generation of biomedical research. It is currently in the prototype stage of development and is under active development.

The goal of Biome is to seamlessly combine the ability to find research data with an ability to deeply analyze it--all from the same user interface. To accomplish this, Biome provides users both a chat and notebook style interface with specialized AI integrations under the hood that enable sophisticated interactions with a variety of biomedical data sources as well as domain specific software libraries and tools. 

Biome is being developed under ARPA-H's [Biomedical Data Fabric (BDF) Toolbox](https://arpa-h.gov/news-and-events/arpa-h-announces-effort-develop-single-data-system-biomedical-research) program.

## Requirements

- docker-compose

## Getting started 

Many environment variables will need to be defined. See `env.sample` for one to copy and paste, and/or consult the same thing inline below.

You will need to add the API keys.

Copy all of `env.sample` to `.env` in the root of the project directory, then add the keys.

Example:  
```
cp env.sample .env
```

The keys are defined at the top. All of the variables that are not necessary to manually change have been omitted below with the ellipses.

```
# API Keys
OPENAI_API_KEY=<your API key>
GEMINI_API_KEY=<your API key>

#
# Deployment Specific
# -- only change below this line if you have special requirements for environment!
#
...
```

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
