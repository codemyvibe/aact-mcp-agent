"""AACT Database Query Agent using MCP Plugin."""

import os
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# Load environment variables from .env file
load_dotenv()

# Define the root agent
root_agent = Agent(
    name="aact_query_agent",
    model="gemini-2.0-flash",
    description="An agent that interacts with the AACT clinical trials database.",
    instruction="""
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
    """,
    # MCPToolset will provide the tools when using adk web
    tools=[]
)

# Note: The MCP Server Configuration is now handled differently.
# We don't define the configuration here because ADK will connect to the server
# via the adk web command when running 