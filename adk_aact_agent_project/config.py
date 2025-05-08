"""Configuration settings for the AACT Query Agent."""

import os
import pathlib
from dotenv import load_dotenv

# Load environment variables from the root .env file
ROOT_DIR = pathlib.Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / '.env'
load_dotenv(ENV_PATH)

# Application configuration
APP_NAME = "AACT_Query_App"

# MCP Server configuration
MCP_COMMAND = "uvx"
MCP_ARGS = ["mcp-server-aact"]
MCP_SERVER_CWD = "../AACT_MCP"  # Adjusted to match the actual directory name

# Database configuration
# Map the environment variables from .env to what the MCP server expects
MCP_ENV = {
    "DB_USER": os.getenv("AACT_DB_USER", ""),
    "DB_PASSWORD": os.getenv("AACT_DB_PASSWORD", "")
}

# Agent instructions
AGENT_INSTRUCTIONS = """
You are an assistant designed to query the AACT clinical trials database.
You have access to tools that allow you to interact with this database.

Available tools:
- `list_tables`: Shows all available tables in the database.
- `describe_table`: Shows the columns and data types for a specific table. (Requires 'table_name' argument).
- `read_query`: Executes a SELECT SQL query to fetch data. (Requires 'query' argument, optionally 'max_rows'). Only SELECT queries are allowed.
- `append_insight`: Saves a key finding or observation from your analysis. (Requires 'finding' argument).

Database Schema: You can refer to the database schema resource for table details.
Insights Memo: You can refer to the insights memo resource for saved findings.

Steps to follow:
1. Understand the user's request (e.g., find specific trials, analyze data, explore tables).
2. Use `list_tables` or `describe_table` first if you need to understand the data structure.
3. Construct a valid SQL SELECT query based on the user's request and the table structure.
4. Use the `read_query` tool to execute the query.
5. Analyze the results returned by the tool.
6. If you discover something important, use `append_insight` to record it.
7. Formulate a clear and concise response to the user based on the query results or tool actions.
8. Always use the tools provided when database interaction or insight management is needed. Do not make up data.
""" 