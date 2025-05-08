# AACT MCP Agent

An AI agent that interacts with the AACT (Aggregate Analysis of ClinicalTrials.gov) database using Google's ADK (Agent Development Kit) and MCP (Model Calling Protocol).

## Overview

This project enables AI agents to query and analyze clinical trial data from the AACT database, providing insights and generating reports through natural language interaction.

## Features

- **Natural Language Querying**: Ask questions about clinical trials in plain English
- **Database Exploration**: List tables, describe schemas, and explore the AACT database structure
- **SQL Query Execution**: Construct and execute SELECT queries against the database
- **Insights Management**: Save key findings and observations for future reference

## Architecture

The project consists of two main components:

1. **AACT Agent** (`aact_agent/`): The ADK-based agent that handles user interactions
2. **MCP Server** (`AACT_MCP/`): The backend server that provides database connectivity

## Prerequisites

- Python 3.10+
- Access to AACT database credentials
- Google ADK installed (`pip install -U google-adk`)
- UV package manager (`pip install uv`)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/codemyvibe/aact-mcp-agent.git
   cd aact-mcp-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your AACT credentials:
   ```
   AACT_DB_USER=your_username
   AACT_DB_PASSWORD=your_password
   ```

## Usage

To run the agent with the ADK web interface:

```bash
adk web --agent-module aact_agent
```

Example queries:
- "List all tables in the database"
- "Describe the structure of the studies table"
- "Find all phase 3 trials related to cancer"
- "How many clinical trials were completed in 2022?"

## Debugging

If you encounter issues, use the debugging scripts:

```powershell
.\debug_all.ps1
```

Or run individual tests:

```powershell
# Test UVX command availability
python aact_agent/test_uvx_command.py

# Test MCP server communication
python aact_agent/json_rpc_test.py

# Test agent functionality
python aact_agent/debug_agent.py

# Improved MCP debugging
python adk_aact_agent_project/debug_mcp_improved.py
```

See `aact_agent/DEBUGGING.md` for detailed troubleshooting steps.

## Common Issues

- **Path Resolution**: Ensure the correct paths to the MCP server
- **Database Connectivity**: Verify credentials and network access
- **Module Import Errors**: Check if all dependencies are installed

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 