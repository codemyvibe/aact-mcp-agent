"""Test JSON-RPC communication with the AACT MCP server."""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the request to list tables
LIST_TABLES_REQUEST = {
    "jsonrpc": "2.0",
    "id": "test_list_tables",
    "method": "list_tables",
    "params": {}
}

async def test_mcp_rpc_communication():
    """Test direct JSON-RPC communication with the MCP server."""
    print("Starting MCP JSON-RPC test...")
    
    # MCP Server Configuration
    MCP_COMMAND = "uvx"
    MCP_ARGS = ["mcp-server-aact"]
    MCP_SERVER_CWD = str(Path(__file__).parents[1] / "AACT_MCP")
    MCP_ENV = {
        "DB_USER": os.getenv("AACT_DB_USER"),
        "DB_PASSWORD": os.getenv("AACT_DB_PASSWORD")
    }
    
    print(f"Starting MCP Server...")
    print(f"  Command: {MCP_COMMAND}")
    print(f"  Args: {MCP_ARGS}")
    print(f"  Working Directory: {os.path.abspath(MCP_SERVER_CWD)}")
    print(f"  Environment: DB_USER={MCP_ENV.get('DB_USER')}, DB_PASSWORD={'*' * len(MCP_ENV.get('DB_PASSWORD', ''))}")
    
    try:
        # Start the MCP server process
        process = await asyncio.create_subprocess_exec(
            MCP_COMMAND, *MCP_ARGS,
            cwd=MCP_SERVER_CWD,
            env={**os.environ, **MCP_ENV},
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        print("MCP server process started, waiting for initialization...")
        
        # Wait a moment for the server to initialize
        await asyncio.sleep(2)
        
        # Send a JSON-RPC request
        print(f"Sending JSON-RPC request: {json.dumps(LIST_TABLES_REQUEST)}")
        process.stdin.write(json.dumps(LIST_TABLES_REQUEST).encode() + b'\n')
        await process.stdin.drain()
        
        # Read the response
        print("Waiting for response...")
        response_line = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
        response = json.loads(response_line)
        
        print(f"Received response: {json.dumps(response, indent=2)}")
        
        # Check if the response contains an error
        if "error" in response:
            print(f"Error received: {response['error']}")
        elif "result" in response:
            print(f"Success! Tables: {response['result']}")
        
        # Send a terminate request to properly close the server
        terminate_request = {"jsonrpc": "2.0", "id": "terminate", "method": "terminate", "params": {}}
        process.stdin.write(json.dumps(terminate_request).encode() + b'\n')
        await process.stdin.drain()
        
        print("Test completed.")
    
    except asyncio.TimeoutError:
        print("ERROR: Timeout waiting for MCP server response")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Make sure the process is terminated
        if 'process' in locals():
            try:
                process.terminate()
                await asyncio.wait_for(process.wait(), timeout=5.0)
            except Exception as ex:
                print(f"Error terminating process: {ex}")

async def test_connection_string():
    """Test database connection string formation."""
    print("\nTesting database connection string...")
    
    db_user = os.getenv("AACT_DB_USER")
    db_password = os.getenv("AACT_DB_PASSWORD")
    
    if not db_user or not db_password:
        print("ERROR: Missing database credentials in environment variables")
        return
    
    connection_string = f"postgresql://{db_user}:{db_password}@aact-db.ctti-clinicaltrials.org/aact"
    masked_connection_string = f"postgresql://{db_user}:{'*'*len(db_password)}@aact-db.ctti-clinicaltrials.org/aact"
    
    print(f"Connection string: {masked_connection_string}")
    
    try:
        # Test if psycopg2 is installed
        import psycopg2
        print("psycopg2 is installed")
        
        # Just verify the connection string formation
        print("Connection string formation tested successfully")
    
    except ImportError:
        print("WARNING: psycopg2 is not installed, cannot test actual connection")

async def check_mcp_server_path():
    """Check if the MCP server path exists."""
    print("\nChecking MCP server path...")
    
    # Try different possible paths
    possible_paths = [
        Path(__file__).parents[1] / "AACT_MCP",
        Path(__file__).parents[1] / "aact_mcp_server",
        Path(__file__).parent / "../AACT_MCP",
        Path.cwd() / "AACT_MCP"
    ]
    
    for path in possible_paths:
        abs_path = path.resolve()
        print(f"Checking: {abs_path}")
        if abs_path.exists():
            print(f"Path exists: {abs_path}")
            
            # Check for server.py
            server_py = abs_path / "src" / "server.py"
            if server_py.exists():
                print(f"Found server.py: {server_py}")
            else:
                print(f"server.py not found in {abs_path / 'src'}")
        else:
            print(f"Path does not exist: {abs_path}")

if __name__ == "__main__":
    print("===== MCP JSON-RPC Test =====")
    asyncio.run(check_mcp_server_path())
    asyncio.run(test_connection_string())
    asyncio.run(test_mcp_rpc_communication())
    print("===== Test Complete =====") 