# Biome 

Codename: `Biome`

Web project to manage registering, browsing, tuning datasources.
- Frontend: Analyst-UI submodule built with Beaker-vue.
- Backend: python 3.11, `poetry` for dependency management and packaging.
- Legacy Frontend: Javascript with Nextjs / Reactjs

## Requirements

- python 3.11
- poetry
- nodejs < 18.17
- docker, with compose plugin

### With NixOS
While a dedicated Nix configuration does not yet exist, you can
get up and running quickly by using [this `flake.nix`](https://gist.github.com/fivegrant/bf87ed495a15d5661881fc1855f3b5bc)
to get a quick and dirty FHS for Python, Poetry and Node.js.

## Getting started 

### Initializization

First run:
```
./init-biome.sh 
```

Then, make sure to give the generated `.ssh/id_rsa` permission to read the 
Jvoy repo. Additionally, update the `OPENAI_ORG_ID` and `OPENAI_API_KEY` in `.env`.
To find the default values for everything, look at `env.sample`.

NOTE: `.ssh/id_rsa` is needed as long as Jvoy remains private. Once Jvoy is a publically
available repo, we'll no longer need SSH.

### Execution

Starting the project with the following command: 
```
docker compose up -d
```

and can be brought down with
```
docker compose down
```

## Usage

Visit http://localhost:8001 in the browser to use
the legacy UI.

Visit http://localhost:8888 to use the WIP Analyst-UI.

### Development

#### Docker
`docker compose build` or `docker compose up --build` are usually sufficient
for rebuilding containers when their dependencies have beeen updated,
but use `docker compose build --no-cache` if you want to force everything to rebuild.
If a container doesn't have hot-reloading, it's usually enough to just the container
down and up again to have the changes reflected.

#### Analyst-UI
To view the Analyst-UI with hot-reloading in browser, please
use http://localhost:8080 instead of http://localhost:8888. 
If `analyst-ui/beaker-ts` is modified, run `make clean; make beaker_kernel/server/ui/index.html`
and rebuild the docker container. Note that `analyst-ui/.env` is NOT
read and the OpenAI key used is the one in the root `.env`.

#### Jobs & Worker
There is an RQ dashboard available at http://localhost:9181. You'll be able to navigate
to a web console and check that everything looks good, as well as inspect the
queued/running/failed jobs (web scraping, etc). With the source for a job is updated,
restarting the container should update the container as well as long as no dependencies
changed.

#### Biome API
Any changes to the backend source should cause the API to hot-reload.


## Architecture

### Services 

- Biome API(8082): A web server implemented in FastAPI to list, retrieve, register new datasources. 

- Workers: Worker code for jobs related to scraping the web data portal / site to characterize
the types of data, formats, possible operations user wants to complete from this site
or even in combination with other sites.

- Analyst-UI(8080): The new WIP frontend for Biome. It's a chat first Beaker interface.

- Beaker Kernel(8888): The Biome beaker context is provided by the kernel.

- Elasticsearch 8.13(9200): Currently used to store the scrape metatadata for each web portal source in JSON format.

- Redis(6379): Used to add queue (using redis queue) of jobs for workers to perform scraping and other operations

- Legacy Frontend + Caddy(8001): User interface to list/review datasources registered, as well as interact with
the web server API to register new datasources.


#### Diagram
```
  backend                                                             
 +-----------------------------------------+                          
 |                                         |                          
 |                   +--------------+      |                          
 |            +------+    Worker    |      |                          
 |            |      +---------+----+      |                          
 |            |           ^    |           |                          
 | (storage)  v           |    v           |                          
 | +-------------+       ++------+         |                          
 | |Elasticsearch|       | Redis | (queue/ |                          
 | +------+------+       +-----+-+  comms) |                          
 |        |               ^    |           |                          
 |        |               |    |           |                          
 |        v               |    v           |                          
 | +----------------------+--------------+ |                          
 | |                                     | |                          
 | |                                     | |                          
 | |              Biome API              | |                          
 | |                                     | |                          
 | |                                     | |                          
 +-+---------------+-------+-------------+-+                          
                ^  |       |  ^                                       
                |  |       |  |                                       
                |  |       |  |                                       
                |  |       |  |  Legacy Frontend                      
Analyst-UI      |  v       |  |  +---------+-------------------------+
+---------------+-----+    |  +--+         |                         |
|    Beaker Kernel    |    |     |  Caddy  |    Next.js+React.js     |
|                     |    +---->|         |                         |
+-----------+---------+          +---------+-------------------------+
|        ^  |         |                                               
|        |  |         |                                               
|        |  v         |                                               
|      +-+-----       |                                               
|      |Vue.js|       |                                               
|      +-------       |                                               
|                     |                                               
+---------------------+  
```

### Backend

While we try to stay light on abstractions, we've adopted two
to make interacting with dependencies / additional services easier.
They are `JobRunner` and `SourcesDatabase`.

`JobRunner` sits in front of Redis and RQ, handling queues and standardizing
messages sent to and from jobs.

`SourcesDatabase` searches and stores Data Sources. Embeddings are generated using
OpenAI and Elasticsearch is used to store the sources. Since embedding usage and retrieval
is very dependent on implementation, Elasticsearch and OpenAI are all used exclusively 
in this object. (The exception if `seeds.json` which probably should be moved to `SourcesDatabase`)

#### Organization of Backend Source
- `backend/lib`: Code used by both Biome API and jobs.
  - `backend/lib/job_runner`: All Redis+RQ-specific is contained here. The API kicks off jobs
                              and reads their status using the Job Runner. The jobs themselves
                              use the runner to write messages to be read by the API.
  - `backend/lib/sources_db`: All Elasticsearch+OpenAI-specific is contained here.
- `backend/worker/jobs.py`: Job code.
- `backend/api`: FastAPI code. 