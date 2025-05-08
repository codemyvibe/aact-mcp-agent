"""Direct test for the agent to list tables."""

import sys
import asyncio
from plugins import aact_mcp_plugin

async def test_list_tables():
    """Test direct interaction with the MCP plugin."""
    try:
        # Start the plugin
        await aact_mcp_plugin.start()
        print("Plugin started successfully")
        
        # Try to list tables
        print("Requesting table list...")
        result = await aact_mcp_plugin.call("list_tables", {})
        
        # Print result
        print(f"Result: {result}")
        
        # Print tables
        if isinstance(result, list):
            print(f"Found {len(result)} tables:")
            for table in result:
                print(f"  - {table}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Stop the plugin
        await aact_mcp_plugin.stop()
        print("Plugin stopped")

if __name__ == "__main__":
    asyncio.run(test_list_tables()) 