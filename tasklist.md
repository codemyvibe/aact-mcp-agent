# Task List: Creating an ADK Agent for AACT_MCP Server

This checklist guides you through setting up the AACT_MCP server project (based on the provided Repomix file) and creating a Google ADK agent to interact with it.

## Phase 1: Set Up the AACT_MCP Server Project

This phase involves recreating the MCP server project locally based on the `repomix-output-tree-main.xml` file you provided.

-   [ ] **1.1. Create Project Directory:** Create a main directory for the MCP server, e.g., `aact_mcp_server`.
-   [ ] **1.2. Recreate Directory Structure:** Inside `aact_mcp_server`, recreate the directory structure shown in `<directory_structure>`:
    ```
    scripts/
    src/
     resources/
     __init__.py
     database.py
     memo_manager.py
     server.py
    .env.example
    .gitignore
    LICENSE
    pyproject.toml
    README.md
    uv.lock
    ```
-   [ ] **1.3. Populate Files:** Copy the code content for each file path provided in the `<files>` section of `repomix-output-tree-main.xml` into the corresponding local files you just created (e.g., copy content for `<file path="src/server.py">` into `aact_mcp_server/src/server.py`).
-   [ ] **1.4. Create Virtual Environment:** Navigate into the `aact_mcp_server` directory in your terminal and create a Python virtual environment:
    ```bash
    python -m venv .venv_mcp
    ```
-   [ ] **1.5. Activate MCP Virtual Environment:** Activate the newly created environment:
    ```bash
    # macOS/Linux
    source .venv_mcp/bin/activate
    # Windows CMD
    # .venv_mcp\Scripts\activate.bat
    # Windows PowerShell
    # .venv_mcp\Scripts\Activate.ps1
    ```
-   [ ] **1.6. Install Dependencies:** Install the required Python packages using the `pyproject.toml` or `uv.lock`. If using `uv` (recommended based on the lock file):
    ```bash
    pip install uv # If you don't have uv installed
    uv pip sync
    ```
    *Alternatively, if not using `uv`, manually install from `pyproject.toml`'s dependencies:*
    ```bash
    # pip install "mcp>=1.5.0" psycopg2-binary python-dotenv
    ```
-   [ ] **1.7. Configure Environment Variables:**
    -   Copy `.env.example` to a new file named `.env` in the `aact_mcp_server` directory.
    -   Edit the `.env` file and add your actual AACT database username and password:
        ```dotenv
        DB_USER=your_aact_username
        DB_PASSWORD=your_aact_password
        ```
-   [ ] **1.8. (Optional) Generate Schema:** If you want to regenerate the `database_schema.json`, run the script (ensure DB credentials are correct in `.env`):
    ```bash
    python scripts/generate_json_schema.py
    ```
-   [ ] **1.9. Test Run MCP Server:** Verify the server can start (it will wait for connections). Run the command defined in `pyproject.toml` under `[project.scripts]` or directly:
    ```bash
    # If using uv configured with the project script:
    # uvx mcp-server-aact
    # Or directly:
    python -m src.server
    ```
    *(Press Ctrl+C to stop it for now)*.

## Phase 2: Set Up the Google ADK Agent Project

This phase involves creating a separate project structure for your Google ADK agent.

-   [X] **2.1. Create ADK Project Directory:** Create a *separate* main directory for the ADK agent, e.g., `adk_aact_agent_project`.
-   [X] **2.2. Create Agent Package:** Inside `adk_aact_agent_project`, create your agent's package directory, e.g., `aact_query_agent`.
-   [X] **2.3. Create `__init__.py`:** Inside `aact_query_agent`, create an `__init__.py` file with the following content:
    ```python
    from . import agent
    ```
-   [X] **2.4. Create `agent.py`:** Inside `aact_query_agent`, create an empty `agent.py` file. We will define the agent in the next phase.
-   [X] **2.5. Create ADK Virtual Environment:** Navigate into the `adk_aact_agent_project` directory in your terminal and create a Python virtual environment:
    ```bash
    python -m venv .venv_adk
    ```
-   [X] **2.6. Activate ADK Virtual Environment:** Activate this environment:
    ```bash
    # macOS/Linux
    source .venv_adk/bin/activate
    # Windows CMD
    # .venv_adk\Scripts\activate.bat
    # Windows PowerShell
    # .venv_adk\Scripts\Activate.ps1
    ```
    *(Ensure you are no longer in the MCP server's virtual environment)*.
-   [X] **2.7. Install ADK:** Install the Google ADK library:
    ```bash
    pip install google-adk python-dotenv
    ```
-   [X] **2.8. Configure ADK Environment:** Create a `.env` file in the `adk_aact_agent_project` directory and add your Google API Key:
    ```dotenv
    GOOGLE_API_KEY=your_google_api_key_here
    ```

## Phase 3: Define the ADK Agent

Now, define the logic for your ADK agent.

-   [X] **3.1. Edit `agent.py`:** Open `adk_aact_agent_project/aact_query_agent/agent.py` and add the following code:
    ```python
    from google.adk.agents import Agent

    # Define the root agent
    root_agent = Agent(
        name="aact_query_agent",
        model="gemini-2.0-flash", # Or another Gemini model
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
        # DO NOT list tools here - the MCPStdioPlugin will provide them.
        tools=[]
    )
    ```

## Phase 4: Create the Runner Script for Integration

Create a script to run the ADK agent and connect it to the MCP server using the plugin.

-   [X] **4.1. Create `run_agent.py`:** In the `adk_aact_agent_project` directory, create a file named `run_agent.py`.
-   [X] **4.2. Edit `run_agent.py`:** Add the following code, **adjusting paths and commands as necessary**:
    ```python
    import asyncio
    import os
    import sys
    from dotenv import load_dotenv

    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService # Or DatabaseSessionService for persistence
    from google.adk.plugins.mcp_stdio_plugin import MCPStdioPlugin
    from google.genai import types

    # Ensure the agent package is importable (adjust path if needed)
    sys.path.append(os.path.dirname(__file__))
    from aact_query_agent import root_agent

    # Load environment variables from .env file (for GOOGLE_API_KEY)
    load_dotenv()

    # --- Configuration ---
    APP_NAME = "AACT_Query_App"
    USER_ID = "test_user"

    # --- !! IMPORTANT: Configure MCP Server Command !! ---
    # Adjust the command and args based on how you run your MCP server
    # Option 1: If using uvx from pyproject.toml
    MCP_COMMAND = "uvx"
    MCP_ARGS = ["mcp-server-aact"]
    # Option 2: If running directly with python
    # MCP_COMMAND = "python"
    # MCP_ARGS = ["-m", "src.server"] # Assumes running from aact_mcp_server dir

    # --- !! IMPORTANT: Path to MCP Server Directory !! ---
    # Adjust this path to point to where your aact_mcp_server project is located
    MCP_SERVER_CWD = "../aact_mcp_server" # Example: if it's one level up

    # --- !! IMPORTANT: MCP Server Environment Variables !! ---
    # Ensure these match your MCP server's .env file
    MCP_ENV = {
        "DB_USER": os.getenv("AACT_DB_USER", "your_aact_username"), # Load from ADK env or default
        "DB_PASSWORD": os.getenv("AACT_DB_PASSWORD", "your_aact_password") # Load from ADK env or default
    }
    # Note: You might need to load DB_USER/PASSWORD into the ADK env or define them here.

    async def main():
        print("Initializing ADK Agent for AACT Database...")

        # 1. Set up the MCP Plugin
        print(f"Configuring MCP Plugin to run command: '{MCP_COMMAND}' with args: {MCP_ARGS}")
        print(f"MCP Server working directory: {os.path.abspath(MCP_SERVER_CWD)}")
        print(f"MCP Server environment DB_USER: {MCP_ENV.get('DB_USER')}")

        aact_mcp_plugin = MCPStdioPlugin(
            name="aact_db_plugin", # Unique name for this plugin instance
            command=MCP_COMMAND,
            args=MCP_ARGS,
            cwd=MCP_SERVER_CWD, # Set the working directory for the server process
            env=MCP_ENV        # Pass necessary environment variables
        )

        # 2. Set up Session Service
        # Using in-memory for simplicity, switch to DatabaseSessionService for persistence
        session_service = InMemorySessionService()
        print("Using InMemorySessionService.")

        # 3. Create or Get Session
        session_id = "session_" + USER_ID # Simple session ID
        try:
            session = session_service.get_session(APP_NAME, USER_ID, session_id)
            print(f"Resuming session: {session_id}")
        except KeyError:
            print(f"Creating new session: {session_id}")
            session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id,
                state={} # Initial state if needed
            )

        # 4. Set up the Runner
        runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=session_service,
            plugins=[aact_mcp_plugin] # Add the plugin
        )
        print("Runner initialized with agent and MCP plugin.")

        # 5. Interaction Loop
        print("\nAgent ready. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting...")
                break

            new_message = types.Content(role="user", parts=[types.Part(text=user_input)])

            print("Agent is thinking...")
            final_response_text = ""
            try:
                async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=new_message):
                    # Simple event logging
                    print(f"  -> Event: {event.id} | Author: {event.author}")
                    if event.is_final_response() and event.content and event.content.parts:
                         if hasattr(event.content.parts[0], 'text'):
                             final_response_text = event.content.parts[0].text
            except Exception as e:
                print(f"\nError during agent run: {e}")
                import traceback
                traceback.print_exc() # Print detailed traceback for debugging

            print(f"\nAgent: {final_response_text}\n")

    if __name__ == "__main__":
        # Ensure you have the ADK virtual environment activated
        print(f"Running ADK agent from directory: {os.getcwd()}")
        print(f"Python executable: {sys.executable}")
        asyncio.run(main())

    ```
-   [X] **4.3. Review Configuration:** Carefully review the `MCP_COMMAND`, `MCP_ARGS`, `MCP_SERVER_CWD`, and `MCP_ENV` variables in `run_agent.py` to ensure they correctly point to and configure your AACT_MCP server setup. You might need to adjust paths (`../aact_mcp_server`) depending on where you placed the two project directories relative to each other. Consider adding the AACT DB credentials to the ADK project's `.env` file (e.g., as `AACT_DB_USER`, `AACT_DB_PASSWORD`) and loading them using `os.getenv` in the `run_agent.py` script for `MCP_ENV`.

## Phase 5: Run and Test

Execute the ADK web command to start interacting with your ADK agent, which should now be able to use the tools provided by the AACT_MCP server.

-   [ ] **5.1. Activate ADK Environment:** Make sure your `.venv_adk` virtual environment is active.
-   [ ] **5.2. Run the Agent with ADK Web:** Navigate to the `aact_agent` directory. Execute the `adk web` command:
    ```bash
    cd aact_agent
    adk web
    ```
    *(This will start a web server at http://localhost:8000, and you can interact with your agent via a browser.)*
-   [ ] **5.3. Test Interaction:** Interact with the agent through the web interface. Try commands that should trigger the MCP tools:
    * "List the available tables."
    * "Describe the 'studies' table."
    * "Show me 5 studies related to diabetes." (This should trigger `read_query`)
    * "Find studies about cancer completed in 2023."
    * "Record this insight: Many recent trials focus on immunotherapy." (This should trigger `append_insight`)
    * "Show me the insights memo."
-   [ ] **5.4. Debug:** Observe the terminal output from both the `run_agent.py` script and potentially the MCP server process (if its logs are visible) to debug any issues with plugin connection or tool execution. Check paths and environment variables if the plugin fails to start the server. Check agent instructions if it fails to use the tools correctly.