"""Debug MCP communication issues between agent and MCP server."""

import asyncio
import os
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / '.env'
load_dotenv(ENV_PATH)

# Database credentials
DB_USER = os.getenv("AACT_DB_USER", "")
DB_PASSWORD = os.getenv("AACT_DB_PASSWORD", "")

# MCP configuration
MCP_COMMAND = "uvx"
MCP_ARGS = ["mcp-server-aact"]
MCP_SERVER_CWD = str(ROOT_DIR / "AACT_MCP")

# MCP server environment
MCP_ENV = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD
}

# Define a simple JSON-RPC request for list_tables
LIST_TABLES_REQUEST = {
    "jsonrpc": "2.0",
    "id": "test-list-tables",
    "method": "list_tables",
    "params": {}
}

async def test_mcp_communication():
    """Test direct communication with MCP server."""
    print("Testing MCP Server Communication")
    print("===============================")
    print(f"Using credentials - User: {DB_USER}")
    
    if not DB_USER or not DB_PASSWORD:
        print("❌ ERROR: Missing database credentials")
        return False
    
    # Start MCP server
    print("\n1. Starting MCP server...")
    env = os.environ.copy()
    env.update(MCP_ENV)
    
    process = subprocess.Popen(
        [MCP_COMMAND] + MCP_ARGS,
        cwd=MCP_SERVER_CWD,
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    print("Waiting for server to initialize...")
    await asyncio.sleep(3)
    
    # Check if process is still running
    if process.poll() is not None:
        print("❌ ERROR: MCP server failed to start")
        stdout, stderr = process.communicate()
        print(f"STDERR: {stderr}")
        return False
    
    print("✅ MCP server started successfully")
    
    # Send a request to list tables
    try:
        print("\n2. Sending list_tables request to MCP server...")
        
        # Convert request to JSON
        request_json = json.dumps(LIST_TABLES_REQUEST) + "\n"
        print(f"Request: {request_json.strip()}")
        
        # Send the request
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Wait for response
        print("Waiting for response...")
        await asyncio.sleep(2)
        
        # Read response
        response_line = process.stdout.readline().strip()
        
        if not response_line:
            print("❌ ERROR: No response received from MCP server")
            print("This suggests a communication issue between the agent and MCP server.")
            return False
            
        print(f"Raw response: {response_line}")
        
        # Parse response
        try:
            response = json.loads(response_line)
            
            if "result" in response:
                tables = response["result"]
                print(f"✅ Successfully received {len(tables)} tables")
                print(f"First 5 tables: {', '.join(tables[:5])}")
                return True
            elif "error" in response:
                print(f"❌ ERROR: {response['error']['message']}")
                return False
            else:
                print("❌ ERROR: Unexpected response format")
                return False
                
        except json.JSONDecodeError:
            print("❌ ERROR: Invalid JSON response")
            return False
    
    except Exception as e:
        print(f"❌ ERROR during communication: {e}")
        return False
    finally:
        # Terminate MCP server
        print("\n3. Terminating MCP server...")
        process.terminate()
        await asyncio.sleep(1)
        print("✅ MCP server terminated")

if __name__ == "__main__":
    success = asyncio.run(test_mcp_communication())
    
    print("\nTest Summary:")
    if success:
        print("✅ MCP communication test PASSED")
        print("The MCP server is functioning correctly and can list tables.")
        print("\nIf your agent still can't list tables, the issue is likely with:")
        print("- How the agent is calling the MCP plugin")
        print("- Plugin configuration in the agent code")
    else:
        print("❌ MCP communication test FAILED")
        print("\nPossible issues:")
        print("1. The MCP server might be configured incorrectly")
        print("2. There might be an issue with the JSON-RPC communication")
        print("3. The database might be restricting access to table information")
        print("\nTry checking the AACT_MCP source code and database permissions.") 