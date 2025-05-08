"""Test MCP client to verify database access.

This script uses the MCP client library directly to test database access
without going through the ADK agent.
"""

import os
import asyncio
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import MCP client libraries
try:
    from mcp.clients import StdioClient
    from mcp.types import Request
except ImportError:
    logger.error("MCP library not found. Please ensure it's installed with: pip install mcp>=1.5.0")
    exit(1)

# Load environment variables
load_dotenv()

# Configuration
MCP_COMMAND = "uvx"
MCP_ARGS = ["mcp-server-aact"]
MCP_SERVER_CWD = "../AACT_MCP"

# Database credentials
DB_USER = os.getenv("AACT_DB_USER", "your_aact_username")
DB_PASSWORD = os.getenv("AACT_DB_PASSWORD", "your_aact_password")

# Environment variables for MCP server
MCP_ENV = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD
}

async def test_list_tables():
    """Test the list_tables functionality."""
    logger.info("Starting MCP server and testing list_tables...")
    
    # Create an MCP client
    client = StdioClient(
        command=MCP_COMMAND,
        args=MCP_ARGS,
        cwd=MCP_SERVER_CWD,
        env=MCP_ENV
    )
    
    try:
        # Start the client
        await client.start()
        logger.info("MCP client started successfully")
        
        # List tables request
        list_tables_request = Request(
            id="test-list-tables-1",
            method="list_tables",
            params={}
        )
        
        # Send the request
        logger.info("Sending list_tables request...")
        response = await client.send_request(list_tables_request)
        
        # Print the response
        logger.info("Received response:")
        logger.info(json.dumps(response, indent=2))
        
        # Check if we got a successful response
        if "result" in response:
            logger.info("SUCCESS: Successfully retrieved tables list")
            
            # Print the list of tables
            if isinstance(response["result"], list):
                logger.info(f"Found {len(response['result'])} tables:")
                for table in response["result"]:
                    logger.info(f"  - {table}")
            else:
                logger.info(f"Result: {response['result']}")
        else:
            logger.error("FAILED: Error in response")
            if "error" in response:
                logger.error(f"Error: {response['error']}")
    
    except Exception as e:
        logger.error(f"Error during test: {e}")
    
    finally:
        # Stop the client
        await client.stop()
        logger.info("MCP client stopped")

async def test_describe_table():
    """Test the describe_table functionality with a sample table."""
    logger.info("Starting MCP server and testing describe_table...")
    
    # Create an MCP client
    client = StdioClient(
        command=MCP_COMMAND,
        args=MCP_ARGS,
        cwd=MCP_SERVER_CWD,
        env=MCP_ENV
    )
    
    try:
        # Start the client
        await client.start()
        logger.info("MCP client started successfully")
        
        # First get a list of tables to pick one for description
        list_tables_request = Request(
            id="test-list-tables-2",
            method="list_tables",
            params={}
        )
        
        tables_response = await client.send_request(list_tables_request)
        
        if "result" in tables_response and isinstance(tables_response["result"], list) and len(tables_response["result"]) > 0:
            # Pick the first table
            sample_table = tables_response["result"][0]
            logger.info(f"Using sample table: {sample_table}")
            
            # Describe table request
            describe_table_request = Request(
                id="test-describe-table-1",
                method="describe_table",
                params={"table_name": sample_table}
            )
            
            # Send the request
            logger.info(f"Sending describe_table request for table: {sample_table}...")
            response = await client.send_request(describe_table_request)
            
            # Print the response
            logger.info("Received response:")
            logger.info(json.dumps(response, indent=2))
            
            # Check if we got a successful response
            if "result" in response:
                logger.info(f"SUCCESS: Successfully described table {sample_table}")
            else:
                logger.error("FAILED: Error in response")
                if "error" in response:
                    logger.error(f"Error: {response['error']}")
        else:
            logger.error("No tables found to describe")
    
    except Exception as e:
        logger.error(f"Error during test: {e}")
    
    finally:
        # Stop the client
        await client.stop()
        logger.info("MCP client stopped")

async def main():
    """Run all tests."""
    await test_list_tables()
    logger.info("-" * 50)
    await test_describe_table()

if __name__ == "__main__":
    asyncio.run(main()) 