"""Test the availability of the uvx command used for the MCP server."""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_uvx_command():
    """Test if the uvx command is available and can be executed."""
    print("Testing 'uvx' command availability...")
    
    try:
        # Try to run a simple uvx command
        process = await asyncio.create_subprocess_exec(
            "uvx", "--help",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            print("SUCCESS: The 'uvx' command is available!")
            print(f"Output from 'uvx --help':\n{stdout.decode().strip()[:500]}...")
        else:
            print(f"ERROR: 'uvx' command execution failed with code {process.returncode}")
            if stderr:
                print(f"Error output: {stderr.decode().strip()}")
        
    except FileNotFoundError:
        print("ERROR: The 'uvx' command was not found.")
        print("Make sure it's installed and available in your PATH.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

async def test_mcp_server_command():
    """Test if the specific MCP server command works."""
    print("\nTesting MCP server command 'uvx mcp-server-aact'...")
    
    # Build the correct path to the MCP server
    current_dir = Path(__file__).parent
    mcp_server_cwd = str((current_dir.parent / "AACT_MCP").resolve())
    
    # Set up environment variables
    mcp_env = {
        **os.environ,
        "DB_USER": os.getenv("AACT_DB_USER", ""),
        "DB_PASSWORD": os.getenv("AACT_DB_PASSWORD", "")
    }
    
    try:
        # Try to run the MCP server command but with --help to avoid actual execution
        process = await asyncio.create_subprocess_exec(
            "uvx", "mcp-server-aact", "--help", 
            cwd=mcp_server_cwd,
            env=mcp_env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=5.0)
        
        # Check if command is recognized
        if process.returncode == 0:
            print("SUCCESS: The 'uvx mcp-server-aact' command is recognized!")
        else:
            print(f"WARNING: 'uvx mcp-server-aact' command returned code {process.returncode}")
        
        if stdout:
            print(f"Standard output:\n{stdout.decode().strip()[:300]}...")
        
        if stderr:
            print(f"Error output:\n{stderr.decode().strip()[:300]}...")
    
    except FileNotFoundError:
        print("ERROR: The 'uvx' command was not found.")
    except asyncio.TimeoutError:
        print("WARNING: Command execution timed out after 5 seconds.")
        print("This might be normal if the server started successfully.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

async def check_module_path():
    """Check Python module path to ensure proper imports."""
    print("\nChecking Python module path...")
    
    # Print Python path
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Print sys.path
    print("\nPython module search paths:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
    
    # Check for specific modules
    modules_to_check = [
        "google.adk",
        "google.adk.tools",
        "google.adk.tools.mcp_tool",
        "google.genai"
    ]
    
    print("\nChecking modules availability:")
    for module_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name} - Found")
        except ImportError as e:
            print(f"  ✗ {module_name} - Not found: {e}")

if __name__ == "__main__":
    print("===== UVX Command Test =====")
    asyncio.run(test_uvx_command())
    asyncio.run(test_mcp_server_command())
    asyncio.run(check_module_path())
    print("===== Test Complete =====") 