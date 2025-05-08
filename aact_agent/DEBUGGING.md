# AACT MCP Agent Debugging Guide

This document provides steps to debug and test the AACT MCP agent.

## Environment Setup

1. Make sure your `.env` file contains the required AACT database credentials:

```
AACT_DB_USER=your_aact_username
AACT_DB_PASSWORD=your_aact_password
```

2. Ensure your Python virtual environment is activated and has all required dependencies.

## Testing Scripts

### 1. Test UVX Command

This script checks if the `uvx` command is available and properly configured:

```powershell
python aact_agent/test_uvx_command.py
```

This will verify:
- If the `uvx` command is installed and accessible
- If the `mcp-server-aact` subcommand is recognized
- If all required Python modules are available

### 2. Test JSON-RPC Communication

This script tests direct JSON-RPC communication with the MCP server:

```powershell
python aact_agent/json_rpc_test.py
```

This will:
- Check if the MCP server path exists
- Test database connection string formation
- Test direct communication with the MCP server using JSON-RPC

### 3. Run Agent Debug Script

This script tests the full agent-MCP communication:

```powershell
python aact_agent/debug_agent.py
```

## Troubleshooting Steps

If you're encountering issues with the agent, try the following troubleshooting steps:

### Path Issues

If the MCP server can't be found:
1. Check that the AACT_MCP directory exists in the correct location
2. Verify that `mcp-server-aact` is installed and available via `uvx`

### Connection Issues

If the database connection fails:
1. Verify your AACT credentials are correct
2. Check for network connectivity to the AACT database
3. Ensure the database host/port is accessible

### Module Import Issues

If you see import errors:
1. Check that all required packages are installed
2. Verify that the virtual environment is properly activated
3. Try reinstalling the ADK package

### JSON-RPC Communication Issues

If the agent can't communicate with the MCP server:
1. Use the `json_rpc_test.py` script to test direct communication
2. Check for any firewall or proxy settings that might block communication
3. Review server logs for error messages

## Running the Agent

After resolving any issues, you can run the agent using:

```powershell
adk web --agent-module aact_agent
``` 