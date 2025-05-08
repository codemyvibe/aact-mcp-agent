"""Agent definition for ADK Web compatibility.

This file makes the agent compatible with the ADK Web framework,
which expects to find a 'root_agent' in a module named 'agent'
at the project root level.
"""

# Re-export the root_agent from the aact_query_agent package
from aact_query_agent import root_agent

# Re-export other required objects
from config import APP_NAME
from plugins import aact_mcp_plugin
from sessions import session_service 