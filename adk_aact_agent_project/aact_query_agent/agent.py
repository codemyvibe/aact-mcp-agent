"""AACT Database Query Agent definition."""

from google.adk.agents import Agent
from ..config import AGENT_INSTRUCTIONS

# Define the root agent
root_agent = Agent(
    name="aact_query_agent",
    model="gemini-2.0-flash", # Or another Gemini model
    description="An agent that interacts with the AACT clinical trials database.",
    instruction=AGENT_INSTRUCTIONS,
    # DO NOT list tools here - the MCPStdioPlugin will provide them.
    tools=[]
) 