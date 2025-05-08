"""Debug script for AACT query agent."""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# Load environment variables
load_dotenv()

async def test_agent():
    """Test the AACT query agent with a specific query."""
    print("Starting agent debug session...")
    
    # MCP Server Configuration
    MCP_COMMAND = "uvx"
    MCP_ARGS = ["mcp-server-aact"]
    
    # Build the correct path to the MCP server
    # Use Path for cross-platform compatibility
    current_dir = Path(__file__).parent
    MCP_SERVER_CWD = str((current_dir.parent / "AACT_MCP").resolve())
    
    MCP_ENV = {
        "DB_USER": os.getenv("AACT_DB_USER", ""),
        "DB_PASSWORD": os.getenv("AACT_DB_PASSWORD", "")
    }
    
    print(f"Connecting to MCP Server...")
    print(f"  Command: {MCP_COMMAND}")
    print(f"  Args: {MCP_ARGS}")
    print(f"  Working Directory: {MCP_SERVER_CWD}")
    print(f"  Environment: DB_USER={MCP_ENV['DB_USER']}, DB_PASSWORD={'*' * len(MCP_ENV['DB_PASSWORD'])}")
    
    try:
        # Connect to MCP server and get tools
        tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command=MCP_COMMAND,
                args=MCP_ARGS,
                cwd=MCP_SERVER_CWD,
                env=MCP_ENV
            )
        )
        
        print(f"Connected to MCP Server successfully!")
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        # Import the agent
        from agent import root_agent
        
        # Assign tools to the agent
        root_agent.tools = tools
        print(f"Assigned {len(tools)} tools to the agent")
        
        # Create a runner
        session_service = InMemorySessionService()
        runner = Runner(
            app_name="AACT_Query_App",
            agent=root_agent,
            session_service=session_service
        )
        
        # Create a session
        session = session_service.create_session(
            app_name="AACT_Query_App",
            user_id="debug_user",
            session_id="debug_session",
            state={}
        )
        
        # Test query
        test_query = "List the available tables in the database."
        print(f"\nSending test query: '{test_query}'")
        
        # Create a message
        message = types.Content(
            role="user",
            parts=[types.Part(text=test_query)]
        )
        
        # Run the agent
        print("Running agent...")
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=message
        ):
            print(f"\nEvent received: Type={event.id}, Author={event.author}")
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        print(f"TEXT: {part.text}")
                    elif hasattr(part, 'function_call') and part.function_call:
                        print(f"FUNCTION CALL: {part.function_call.name}({part.function_call.args})")
                    elif hasattr(part, 'function_response') and part.function_response:
                        print(f"FUNCTION RESPONSE: {part.function_response}")
        
        print("\nTest completed successfully!")
    
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if 'exit_stack' in locals():
            print("\nCleaning up resources...")
            await exit_stack.aclose()

if __name__ == "__main__":
    print("===== AACT Query Agent Debug =====")
    asyncio.run(test_agent())
    print("===== Debug Session Complete =====") 