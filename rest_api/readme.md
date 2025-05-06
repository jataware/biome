# Biome Rest API

FastAPI service for exposing Biome Integrations through a REST interface.

## Deployment

### Docker

`docker-compose.yml` in the biome root will run this service with default values for env vars, requiring only `OPENAI_API_KEY` set in `.env` such as how `.env.sample` does it.

### Env Vars

Be sure to set the following:

| Variable | Value |
| --- | --- |
| `OPENAI_API_KEY` | Used for the Biome agent |
| `BIOME_INTEGRATIONS_DIR` | Point this to the folder that contains Biome's integrations. By default, it will be pointed to `../src/biome/datasources/ such that if you run this from project root it will be in the correct place. |
| `BIOME_DATA_DIR` | Point this to the Git LFS large datasets used with Biome. By default, it will be pointed to `../data` such that if you run this from project root it will be in the correct place. |

### Usage

Run this service as you would any other FastAPI service.

(FastAPI docs)[https://fastapi.tiangolo.com/#run-it]

Install the dependencies with hatch/uv/poetry or any other pyproject.toml and run it with the correct environment variables.

Example (hatch)

```
$ hatch shell
$ fastapi run biome_rest/main.py
```

## Endpoints

#### GET `/list_integrations`

Returns an object containing all of the integrations.

Top level keys are the reference ID used for `integration` fields in the following call, where `name` is a user-facing name for the integration.

```json
{
    "first_integration": {
        "name": "First Integration",
        "description": "The first integration is an API that is used for..."
    },
    "second_integration": {
        "name": "Second Integration",
        "description": "The second integration is an API that is used for..."
    },
}
```

#### GET `/consult_integration_documentation/{integration}`

**Parameters**

`query`: query parameter containing the question to ask the specialist agent.

**Details**

Returns a string inside the top level `response` answering the query provided.

Example:

`/consult_integration_documentation/big_dataset?query=Can the big dataset integration be used to answer questions about this specific topic`

```json
{
    "response": "The integration 'Big Dataset' does have the capability of doing..."
}
```

##### GET `/draft_integration_code/{integration}`

**Parameters**

`query`: query parameter containing the task for the specialist agent to write code for.

**Details**

Returns a string inside the top level `response` containing valid python code to accomplish the task.

Example:

`/consult_integration_documentation/big_database?query=Can you fetch studies related to this specific topic?`

```json
{
    "response": "<python code to accomplish the task>"
}
```
