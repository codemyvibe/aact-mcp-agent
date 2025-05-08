"""Test the agent's ability to access the AACT database through MCP."""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add the parent directory to the path so we can import project modules
sys.path.append(str(Path(__file__).parent))

# Import agent components
from plugins import aact_mcp_plugin
from config import APP_NAME

async def test_agent_database_access():
    """Test if the agent can access the database through the MCP plugin."""
    print("Testing agent's database access through MCP plugin")
    print("================================================")
    
    try:
        # Start the MCP plugin
        print("\n1. Starting MCP plugin...")
        await aact_mcp_plugin.start()
        print("   ✅ MCP plugin started successfully")

        # Test list_tables function
        print("\n2. Testing list_tables function...")
        tables = await aact_mcp_plugin.call("list_tables", {})
        
        if not isinstance(tables, list) or len(tables) == 0:
            print("   ❌ Failed to list tables")
            print(f"   Response: {tables}")
            return False
            
        print(f"   ✅ Successfully listed {len(tables)} tables")
        print("   First 5 tables:", ", ".join(tables[:5]))
        
        # Test describe_table function with the first table
        sample_table = tables[0]
        print(f"\n3. Testing describe_table function with '{sample_table}'...")
        table_schema = await aact_mcp_plugin.call("describe_table", {"table_name": sample_table})
        
        if not table_schema:
            print(f"   ❌ Failed to describe table '{sample_table}'")
            return False
            
        print(f"   ✅ Successfully described table '{sample_table}'")
        print(f"   Found {len(table_schema)} columns")
        print("   First 3 columns:", ", ".join([col["name"] for col in table_schema[:3]]))
        
        # Test a simple SQL query
        print("\n4. Testing read_query function with a simple query...")
        query = f"SELECT * FROM {sample_table} LIMIT 5"
        result = await aact_mcp_plugin.call("read_query", {"query": query})
        
        if not result or "data" not in result:
            print(f"   ❌ Failed to execute query: {query}")
            print(f"   Response: {result}")
            return False
            
        print(f"   ✅ Successfully executed query")
        row_count = len(result["data"])
        print(f"   Retrieved {row_count} rows from {sample_table}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Stop the MCP plugin
        print("\n5. Stopping MCP plugin...")
        try:
            await aact_mcp_plugin.stop()
            print("   ✅ MCP plugin stopped")
        except Exception as e:
            print(f"   ❌ Error stopping MCP plugin: {e}")

if __name__ == "__main__":
    print("AACT Database Agent Access Test")
    print("==============================")
    print("This test verifies that the agent can access the AACT database through the MCP plugin.")
    
    # Load environment variables before running the test
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
        
        db_user = os.getenv('AACT_DB_USER')
        db_password = os.getenv('AACT_DB_PASSWORD')
        print(f"Database credentials - User: {'<set>' if db_user else '<not set>'}, Password: {'<set>' if db_password else '<not set>'}")
    else:
        print(f"❌ Warning: .env file not found at {env_path}")
        
    # Run the test
    success = asyncio.run(test_agent_database_access())
    
    # Print final summary
    print("\nTest Summary:")
    if success:
        print("✅ PASSED: Agent can successfully access the AACT database through MCP")
    else:
        print("❌ FAILED: Agent cannot access the AACT database through MCP")
        print("\nPossible issues:")
        print("1. Database credentials may be incorrect - check .env file")
        print("2. MCP plugin configuration may be incorrect")
        print("3. Network connectivity issues to AACT database server")
        print("4. Python environment missing required dependencies") 