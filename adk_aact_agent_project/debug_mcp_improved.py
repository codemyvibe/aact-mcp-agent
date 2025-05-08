"""Improved debug script for MCP communication issues with longer timeouts."""

import asyncio
import os
import sys
import json
import time
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

async def read_process_output(process, timeout=5.0):
    """Read process output with timeout."""
    start_time = time.time()
    output_lines = []
    
    while time.time() - start_time < timeout:
        line = process.stdout.readline()
        if not line:
            await asyncio.sleep(0.1)
            continue
            
        output_lines.append(line.strip())
        if len(output_lines) > 0:
            return output_lines
            
    return output_lines

async def test_mcp_communication():
    """Test direct communication with MCP server."""
    print("Testing MCP Server Communication")
    print("===============================")
    print(f"Using credentials - User: {DB_USER}")
    print(f"MCP server directory: {MCP_SERVER_CWD}")
    
    if not DB_USER or not DB_PASSWORD:
        print("❌ ERROR: Missing database credentials")
        return False
    
    # Start MCP server
    print("\n1. Starting MCP server...")
    env = os.environ.copy()
    env.update(MCP_ENV)
    
    try:
        process = subprocess.Popen(
            [MCP_COMMAND] + MCP_ARGS,
            cwd=MCP_SERVER_CWD,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    except FileNotFoundError:
        print(f"❌ ERROR: MCP command '{MCP_COMMAND}' not found")
        print("Is uvx installed? Try: pip install uv")
        return False
    except Exception as e:
        print(f"❌ ERROR starting MCP server: {e}")
        return False
    
    # Wait for server to start
    print("Waiting for server to initialize...")
    await asyncio.sleep(5)  # Longer wait time
    
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
        
        # Wait for response with longer timeout
        print("Waiting for response (up to 10 seconds)...")
        response_lines = await read_process_output(process, timeout=10.0)
        
        if not response_lines:
            print("❌ ERROR: No response received from MCP server")
            print("This suggests a communication issue between the agent and MCP server.")
            
            # Check stderr for any errors
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"Error output from server: {stderr_output}")
                
            return False
        
        # Process the first line as a response
        response_line = response_lines[0]    
        print(f"Raw response: {response_line}")
        
        # Parse response
        try:
            response = json.loads(response_line)
            
            if "result" in response:
                tables = response["result"]
                print(f"✅ Successfully received {len(tables)} tables")
                print("First 5 tables:", ", ".join(tables[:5] if tables and len(tables) >= 5 else tables))
                return True
            elif "error" in response:
                print(f"❌ ERROR: {response['error'].get('message', 'Unknown error')}")
                return False
            else:
                print("❌ ERROR: Unexpected response format")
                print(f"Full response: {response}")
                return False
                
        except json.JSONDecodeError:
            print("❌ ERROR: Invalid JSON response")
            print(f"Response text: {response_line}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR during communication: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Terminate MCP server
        print("\n3. Terminating MCP server...")
        process.terminate()
        await asyncio.sleep(1)
        
        if process.poll() is None:
            process.kill()
            print("   Process killed")
        else:
            print("   Process terminated normally")

if __name__ == "__main__":
    success = asyncio.run(test_mcp_communication())
    
    print("\nTest Summary:")
    if success:
        print("✅ MCP communication test PASSED")
        print("The MCP server is functioning correctly and can list tables.")
        print("\nIf your agent still can't list tables, the issue is likely with:")
        print("1. How the agent is communicating with the MCP plugin")
        print("2. Plugin configuration in the agent code")
        print("3. Environmental issues (verify Python paths, ADK installation)")
        print("\nThe key thing is that the MCP server itself works correctly,")
        print("but the agent might not be configured to use it properly.")
    else:
        print("❌ MCP communication test FAILED")
        print("\nPossible issues:")
        print("1. The MCP server might be configured incorrectly")
        print("2. The database credentials might not have sufficient permissions")
        print("3. There might be an issue with the JSON-RPC communication protocol")
        print("4. Check that the uvx command works and can find the MCP server module")
        
        # Print instructions to get more logs
        print("\nTo get more detailed logs, try running the MCP server directly:")
        print(f"cd {MCP_SERVER_CWD}")
        print(f"{MCP_COMMAND} {' '.join(MCP_ARGS)}") 