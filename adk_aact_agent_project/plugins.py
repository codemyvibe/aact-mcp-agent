"""Plugin configuration for the AACT Query Agent."""

from google.adk.plugins.mcp_stdio_plugin import MCPStdioPlugin
from .config import MCP_COMMAND, MCP_ARGS, MCP_SERVER_CWD, MCP_ENV

# MCP Plugin Instance
aact_mcp_plugin = MCPStdioPlugin(
    name="aact_db_plugin",
    command=MCP_COMMAND,
    args=MCP_ARGS,
    cwd=MCP_SERVER_CWD,
    env=MCP_ENV
) 