"""Web runner configuration for the AACT Query Agent.

This module provides the necessary configuration for running the agent 
with the 'adk web' command.
"""

from aact_query_agent import root_agent
from config import APP_NAME
from plugins import aact_mcp_plugin
from sessions import session_service

# These objects are automatically discovered when running 'adk web'
# No explicit functions needed - ADK Web framework handles everything

# Export required objects
__all__ = [
    'root_agent',      # Agent definition  
    'APP_NAME',        # Application name
    'aact_mcp_plugin', # Plugin instance
    'session_service'  # Session service
] 