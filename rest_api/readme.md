# Biome Rest API

FastAPI service for exposing Biome Integrations through a REST interface.

Make sure the MCP client has a timeout set to 30 seconds or higher!

## Quick Start

1. **Start the REST API:**
```bash
# From project root
docker-compose up rest_api
```
REST API will be available at http://localhost:8000

2. **Test the MCP wrapper (optional):**
```bash
# In another terminal
cd rest_api
npx @modelcontextprotocol/inspector python mcp_server.py
```
MCP Inspector UI will be available at http://127.0.0.1:6274

## Environment Setup

Set `OPENAI_API_KEY` in a `.env` file (see `.env.sample` for example).

## Local Development

```bash
cd rest_api
pip install -e .
fastapi run biome_rest/main.py
```

## MCP Server

**⚠️ Important: The REST API must be running first!**

The MCP server is just a wrapper around the REST API that makes it easier for AI assistants to use.

### For Testing:
```bash
# Make sure REST API is running first!
npx @modelcontextprotocol/inspector python mcp_server.py
```
Then open http://127.0.0.1:6274

### For Claude Desktop:
Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "biome": {
      "command": "python",
      "args": ["/path/to/biome-oct-24/rest_api/mcp_server.py"]
    }
  }
}
```

### Available Tools:
- `biome_list_integrations` - Lists all integrations
- `biome_consult_integration_documentation` - Ask questions about integrations
- `biome_draft_integration_code` - Generate Python code

## REST API Endpoints

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
