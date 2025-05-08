"""Console runner for the AACT Query Agent."""

import asyncio
import sys
from google.adk.runners import Runner
from google.genai import types

from aact_query_agent import root_agent
from config import APP_NAME
from plugins import aact_mcp_plugin
from sessions import session_service, get_or_create_session

async def main():
    """Run the AACT Query Agent in console mode."""
    print("Initializing ADK Agent for AACT Database...")
    
    # Set up the Runner with our agent, plugin, and session service
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        plugins=[aact_mcp_plugin]
    )
    print("Runner initialized with agent and MCP plugin.")
    
    # Default user for console mode
    user_id = "console_user"
    session_id = f"session_{user_id}"
    
    # Get or create session
    get_or_create_session(user_id, session_id)
    
    # Interaction Loop
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
            async for event in runner.run_async(
                user_id=user_id, 
                session_id=session_id, 
                new_message=new_message
            ):
                if event.type == "error":
                    print(f"Error: {event.error}")
                    break
                
                if event.type == "intermediate_response":
                    # For streaming responses (optional)
                    if event.text:
                        print(f"(Thinking): {event.text}")
                
                if event.type == "final_response":
                    final_response_text = event.response.text()
            
            if final_response_text:
                print(f"\nAgent: {final_response_text}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 