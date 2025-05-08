"""AACT Database Query Agent"""

import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from .agent import root_agent

# Load environment variables
load_dotenv()

# Define the async function to create an agent with MCP tools
async def create_agent():
    """Get ADK agent with MCP tools attached."""
    # MCP Server Configuration
    MCP_COMMAND = "uvx"
    MCP_ARGS = ["mcp-server-aact"]
    
    # Build the correct path to the MCP server
    # Use Path for cross-platform compatibility
    current_dir = Path(__file__).parent
    MCP_SERVER_CWD = str((current_dir.parent / "AACT_MCP").resolve())
    
    MCP_ENV = {
        "DB_USER": os.getenv("AACT_DB_USER", ""),
        "DB_PASSWORD": os.getenv("AACT_DB_PASSWORD", "")
    }
    
    # Connect to MCP server and get tools
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command=MCP_COMMAND,
            args=MCP_ARGS,
            cwd=MCP_SERVER_CWD,
            env=MCP_ENV
        )
    )
    
    # Add the tools to the root agent
    root_agent.tools = tools
    
    # Return the agent and exit stack for proper cleanup
    return root_agent, exit_stack

# This is the variable that ADK web will look for
root_agent = create_agent 