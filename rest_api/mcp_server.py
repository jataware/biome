#!/usr/bin/env python3
"""
MCP Server wrapper for Biome REST API

This server provides Model Context Protocol (MCP) tools that wrap the Biome FastAPI endpoints,
making them more readily accessible to AI assistants.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import httpx
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default base URL for the Biome REST API
DEFAULT_BASE_URL = "http://localhost:8000"

class BiomeMCPServer:
    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.server = Server("biome-mcp-server")
        self._setup_tools()

    def _setup_tools(self):
        """Register MCP tools for each Biome endpoint"""
        
        @self.server.list_tools()
        async def list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name="biome_list_integrations",
                    description="List all available Biome integrations and their descriptions",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="biome_consult_integration_documentation",
                    description="Ask questions about a specific integration's capabilities and usage",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "integration": {
                                "type": "string",
                                "description": "The integration ID to query (use biome_list_integrations to see available options)"
                            },
                            "query": {
                                "type": "string",
                                "description": "The question to ask about the integration"
                            }
                        },
                        "required": ["integration", "query"]
                    }
                ),
                types.Tool(
                    name="biome_draft_integration_code",
                    description="Generate Python code to accomplish a task using a specific integration",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "integration": {
                                "type": "string",
                                "description": "The integration ID to use (use biome_list_integrations to see available options)"
                            },
                            "query": {
                                "type": "string",
                                "description": "The task description for which to generate Python code"
                            }
                        },
                        "required": ["integration", "query"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            try:
                if name == "biome_list_integrations":
                    result = await self._list_integrations()
                elif name == "biome_consult_integration_documentation":
                    integration = arguments.get("integration")
                    query = arguments.get("query")
                    if not integration or not query:
                        raise ValueError("Both 'integration' and 'query' are required")
                    result = await self._consult_integration_documentation(integration, query)
                elif name == "biome_draft_integration_code":
                    integration = arguments.get("integration")
                    query = arguments.get("query")
                    if not integration or not query:
                        raise ValueError("Both 'integration' and 'query' are required")
                    result = await self._draft_integration_code(integration, query)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [types.TextContent(type="text", text=result)]
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request to the Biome REST API"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making {method} request to: {url} with params: {params}")
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                logger.info(f"Response status: {response.status_code}")
                response.raise_for_status()
                return response.json()
            except httpx.ConnectError as e:
                logger.error(f"Connection failed to {url}: {e}")
                raise Exception(f"Failed to connect to Biome API at {url}. Is the FastAPI server running?")
            except httpx.TimeoutException as e:
                logger.error(f"Request timeout to {url}: {e}")
                raise Exception(f"Request to Biome API timed out: {str(e)}")
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise Exception(f"API request failed: {e.response.status_code} {e.response.text}")
            except Exception as e:
                logger.error(f"Unexpected error for {url}: {type(e).__name__}: {e}")
                raise Exception(f"Failed to connect to Biome API: {str(e)}")

    async def _list_integrations(self) -> str:
        """List all available integrations"""
        try:
            data = await self._make_request("GET", "/list_integrations")
            
            # Format the response for better readability
            result = "Available Biome Integrations:\n\n"
            for integration_id, details in data.items():
                for name, description in details.items():
                    result += f"**{integration_id}** - {name}\n"
                    result += f"Description: {description}\n\n"
            
            return result
        except Exception as e:
            return f"Error listing integrations: {str(e)}"

    async def _consult_integration_documentation(self, integration: str, query: str) -> str:
        """Consult integration documentation"""
        try:
            logger.info(f"Consulting documentation for {integration} with query: {query}")
            params = {"query": query}
            data = await self._make_request("GET", f"/consult_integration_documentation/{integration}", params)
            response = data.get("response", "No response received")
            logger.info(f"Documentation consultation completed for {integration}")
            return response
        except Exception as e:
            logger.error(f"Documentation consultation failed for {integration}: {e}")
            return f"Error consulting integration documentation: {str(e)}"

    async def _draft_integration_code(self, integration: str, query: str) -> str:
        """Draft integration code"""
        try:
            logger.info(f"Drafting code for {integration} with query: {query}")
            params = {"query": query}
            data = await self._make_request("GET", f"/draft_integration_code/{integration}", params)
            code = data.get("response", "No code generated")
            logger.info(f"Code generation completed for {integration}")
            
            # Format the code response
            return f"Generated Python code for task '{query}' using integration '{integration}':\n\n```python\n{code}\n```"
        except Exception as e:
            logger.error(f"Code generation failed for {integration}: {e}")
            return f"Error drafting integration code: {str(e)}"

    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, 
                write_stream, 
                self.server.create_initialization_options()
            )

async def main():
    """Main entry point"""
    import os
    
    # Allow configuration of the base URL via environment variable
    base_url = os.getenv("BIOME_API_BASE_URL", DEFAULT_BASE_URL)
    
    logger.info(f"Starting Biome MCP Server with base URL: {base_url}")
    logger.info("Server is ready and waiting for MCP client connections...")
    
    server = BiomeMCPServer(base_url)
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())