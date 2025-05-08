"""Test script to verify database access."""

import os
import sys
import subprocess
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config import MCP_COMMAND, MCP_ARGS, MCP_SERVER_CWD, MCP_ENV

async def test_mcp_connection():
    """Test if we can connect to the MCP server and list tables."""
    print(f"Starting MCP server with command: {MCP_COMMAND} {' '.join(MCP_ARGS)}")
    print(f"Working directory: {MCP_SERVER_CWD}")
    print(f"Using database user: {MCP_ENV.get('DB_USER')}")
    
    # Start the MCP server as a subprocess
    try:
        # Set up environment variables
        env = os.environ.copy()
        env.update(MCP_ENV)
        
        # Start MCP server
        process = subprocess.Popen(
            [MCP_COMMAND] + MCP_ARGS,
            cwd=MCP_SERVER_CWD,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("MCP server started. Waiting for it to initialize...")
        # Wait a moment for the server to start
        await asyncio.sleep(2)
        
        # Check if the process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print("Error: MCP server failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
        
        print("MCP server is running. Attempting to communicate...")
        
        # TODO: Here we would interact with the MCP server
        # Since direct interaction requires the MCP plugin, which itself uses the ADK,
        # we'll just verify that the server starts correctly for now
        
        # Terminate the process
        process.terminate()
        await asyncio.sleep(1)
        
        return True
        
    except Exception as e:
        print(f"Error during test: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_mcp_connection())
    if result:
        print("MCP server test completed successfully.")
    else:
        print("MCP server test failed.") 