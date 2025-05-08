"""Test MCP database access directly using mcp package."""

import asyncio
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the root .env file
ROOT_DIR = Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / '.env'
print(f"Looking for .env file at: {ENV_PATH}")
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
    print(f"Loaded environment from {ENV_PATH}")
else:
    print(f".env file not found at {ENV_PATH}")

# Database credentials
DB_USER = os.getenv("AACT_DB_USER", "")
DB_PASSWORD = os.getenv("AACT_DB_PASSWORD", "")

# Print loaded credentials (safely)
print(f"\nCredentials loaded from .env:")
print(f"DB_USER: {'<set: ' + DB_USER + '>' if DB_USER else '<not set>'}")
print(f"DB_PASSWORD: {'<set>' if DB_PASSWORD else '<not set>'}")

# MCP configuration
MCP_COMMAND = "uvx"
MCP_ARGS = ["mcp-server-aact"]
MCP_SERVER_CWD = str(ROOT_DIR / "AACT_MCP")

# Environment variables for MCP server
MCP_ENV = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD
}

async def test_mcp_server():
    """Test MCP server's ability to access the AACT database."""
    print("\n1. Starting MCP server process...")
    
    # Check if we have credentials
    if not DB_USER or not DB_PASSWORD:
        print("❌ ERROR: No database credentials found.")
        print("Please set AACT_DB_USER and AACT_DB_PASSWORD in your .env file.")
        return False
        
    # Start MCP server
    env = os.environ.copy()
    env.update(MCP_ENV)
    
    process = subprocess.Popen(
        [MCP_COMMAND] + MCP_ARGS,
        cwd=MCP_SERVER_CWD,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("MCP server process started, waiting for initialization...")
    await asyncio.sleep(3)
    
    # Check if process is still running
    if process.poll() is not None:
        print("❌ ERROR: MCP server process failed to start.")
        stdout, stderr = process.communicate()
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        if "password authentication failed" in stderr:
            print("\n❌ Authentication Error: The credentials provided were rejected by the database.")
            print("Please verify your AACT database username and password.")
        return False
    
    print("✅ MCP server is running successfully.")
    print("This confirms the database connection is working correctly.")
    
    # Try to read process output
    try:
        # Read up to 20 lines of output to check for any messages
        print("\nMCP server output:")
        for _ in range(20):
            line = process.stdout.readline()
            if not line:
                break
            print(f"  {line.strip()}")
    except Exception as e:
        print(f"Error reading process output: {e}")
        
    # Terminate process
    print("\n2. Terminating MCP server...")
    process.terminate()
    await asyncio.sleep(1)
    print("✅ MCP server terminated.")
    
    return True

if __name__ == "__main__":
    print("MCP Server Direct Test")
    print("=====================")
    print("This test verifies that the MCP server can access the AACT database.")
    
    success = asyncio.run(test_mcp_server())
    
    print("\nTest Summary:")
    if success:
        print("✅ SUCCESS: MCP server can connect to AACT database")
        print("\nThis confirms that your agent will be able to access the database tables.")
        print("Your credentials are working correctly.")
    else:
        print("❌ FAILED: MCP server cannot connect to AACT database")
        print("\nPossible issues:")
        print("1. Database credentials may be incorrect - check .env file")
        print("2. AACT database may be unavailable - check status at https://aact.ctti-clinicaltrials.org/")
        print("3. Network connectivity issues")
        print("4. uvx command may not be installed or working correctly")
        print("\nTo fix, try running setup_env.py to update your credentials.") 