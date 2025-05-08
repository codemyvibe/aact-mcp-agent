"""Basic MCP test script."""

import os
import asyncio
import json
import subprocess
import pathlib
from dotenv import load_dotenv

# Get the root directory and load environment variables
ROOT_DIR = pathlib.Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / '.env'
print(f"Looking for .env file at: {ENV_PATH}")
print(f"File exists: {ENV_PATH.exists()}")
load_dotenv(ENV_PATH)

# Configuration
MCP_COMMAND = "uvx"
MCP_ARGS = ["mcp-server-aact"]
MCP_SERVER_CWD = "../AACT_MCP"

# Database credentials from .env
DB_USER = os.getenv("AACT_DB_USER", "")
DB_PASSWORD = os.getenv("AACT_DB_PASSWORD", "")

# Print loaded credentials (safely)
print(f"\nCredentials loaded from .env:")
print(f"DB_USER: {'<set: ' + DB_USER + '>' if DB_USER else '<not set>'}")
print(f"DB_PASSWORD: {'<set>' if DB_PASSWORD else '<not set>'}")

# Environment variables for MCP server
MCP_ENV = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD
}

async def test_mcp():
    """Test basic MCP functionality."""
    print("\nStarting MCP server test...")
    
    # Check if we have credentials
    if not DB_USER or not DB_PASSWORD:
        print("\n⚠️ ERROR: No database credentials provided.")
        print("You need to register at https://aact.ctti-clinicaltrials.org/ to get valid credentials.")
        print("Then run the setup_env.py script to save your credentials to the .env file.")
        return False
    
    # Start MCP server in subprocess
    env = os.environ.copy()
    env.update(MCP_ENV)
    
    # Launch MCP server
    process = subprocess.Popen(
        [MCP_COMMAND] + MCP_ARGS,
        cwd=MCP_SERVER_CWD,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("MCP server process started, waiting for initialization...")
    # Wait a moment for server to start
    await asyncio.sleep(3)
    
    # Check if process started properly
    if process.poll() is not None:
        print("Error: MCP server failed to start")
        stdout, stderr = process.communicate()
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        if "password authentication failed" in stderr:
            print("\n⚠️ Authentication Error: The credentials provided were rejected by the database.")
            print("Please verify your AACT database username and password.")
        return False
    
    # At this point the server should be running
    print("✅ MCP server is running. This indicates it can connect to the database.")
    print(f"Using database user: {DB_USER}")
    
    # Wait a moment more
    await asyncio.sleep(1)
    
    # Clean up
    print("Test complete. Terminating MCP server...")
    process.terminate()
    await asyncio.sleep(1)
    
    return True

if __name__ == "__main__":
    print("AACT MCP Server Test")
    print("===================")
    print("This test checks if the MCP server can connect to the AACT database.")
    print("You need personal credentials to access this database.")
    print("Register at: https://aact.ctti-clinicaltrials.org/")
    
    success = asyncio.run(test_mcp())
    
    # Print summary
    print("\nTest Summary:")
    print(f"- MCP server / database access: {'✅ Successful' if success else '❌ Failed'}")
    
    if not success:
        print("\nTo set up your credentials:")
        print("1. Register at https://aact.ctti-clinicaltrials.org/")
        print("2. Run the setup script: python setup_env.py")
        print("3. Enter your AACT username and password when prompted")
        print("\nThen run this test again to verify the connection.") 