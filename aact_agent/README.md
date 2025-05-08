# AACT Database Query Agent

This agent connects to the AACT clinical trials database via an MCP server and provides tools to query and analyze clinical trial data.

## Setup

1. Make sure the MCP server is set up according to Phase 1 of the tasklist.
2. Ensure your `.env` file contains:
   - `GOOGLE_API_KEY`: Your Google API key for the Gemini model
   - `AACT_DB_USER`: Your AACT database username
   - `AACT_DB_PASSWORD`: Your AACT database password

## Running the Agent

To run the agent with the web interface:

```bash
# Make sure you're in the root directory of the project
cd aact_agent
adk web
```

This will start a web server and provide a URL (typically http://localhost:8000).

## Testing the Agent

Try these sample prompts:

- "List the available tables."
- "Describe the 'studies' table."
- "Show me 5 studies related to diabetes."
- "Find studies about cancer completed in 2023."
- "Record this insight: Many recent trials focus on immunotherapy."
- "Show me the insights memo." 