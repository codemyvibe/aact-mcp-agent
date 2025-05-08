# AACT Query Agent

This agent allows you to query the AACT clinical trials database using natural language.

## Project Structure

The project is organized following clean architecture principles:

```
adk_aact_agent_project/
├── aact_query_agent/       # Core agent package
│   ├── __init__.py         # Package exports
│   └── agent.py            # Agent definition
├── config.py               # Configuration settings
├── plugins.py              # Plugin configuration
├── sessions.py             # Session management
├── run_agent.py            # Console runner
├── web_runner.py           # ADK Web configuration
├── agent.py                # Root-level agent for ADK Web compatibility
└── README.md               # This file
```

## Running the Agent

### Console Mode

Run the agent in console mode:

```bash
python run_agent.py
```

### Web Mode

Run the agent using ADK Web:

```bash
adk web
```

## Configuration

Edit the `config.py` file to modify settings:

- `APP_NAME`: The name of the application
- `MCP_COMMAND`, `MCP_ARGS`, `MCP_SERVER_CWD`: MCP server configuration
- `MCP_ENV`: Database connection information
- `AGENT_INSTRUCTIONS`: The agent's system instructions

## Environment Setup

1. Create a `.env` file in the project root with the following content:

```
# Google API key for the ADK
GOOGLE_API_KEY=your_google_api_key_here

# AACT Database credentials
AACT_DB_USER=your_aact_username
AACT_DB_PASSWORD=your_aact_password
```

2. Make sure the AACT_MCP server has the correct database credentials in its `.env` file.

3. Install required dependencies:

```bash
pip install "google-adk>=0.4.0" "mcp>=1.5.0" python-dotenv
```

## Testing Database Access

You can test database access with:

```bash
python direct_test.py
```

This will attempt to connect to the MCP server and list available tables. 