"""Direct test of AACT database connection using psycopg2."""

import os
import sys
import pathlib
import subprocess
from dotenv import load_dotenv

# Get the root directory and load environment variables
ROOT_DIR = pathlib.Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / '.env'
print(f"Looking for .env file at: {ENV_PATH}")
print(f"File exists: {ENV_PATH.exists()}")
load_dotenv(ENV_PATH)

# Database credentials
DB_USER = os.getenv("AACT_DB_USER", "")
DB_PASSWORD = os.getenv("AACT_DB_PASSWORD", "")

print(f"\nCredentials loaded from .env:")
print(f"DB_USER: {'<set: ' + DB_USER + '>' if DB_USER else '<not set>'}")
print(f"DB_PASSWORD: {'<set>' if DB_PASSWORD else '<not set>'}")

# Database connection parameters
DB_HOST = "aact-db.ctti-clinicaltrials.org"
DB_PORT = "5432"
DB_NAME = "aact"

def test_psycopg2_connection():
    """Test direct connection to the database using psycopg2."""
    try:
        import psycopg2
        print("\nTesting direct psycopg2 connection...")
        print(f"Connecting to {DB_HOST}:{DB_PORT}/{DB_NAME} as {DB_USER}")
        
        # Check if we have credentials
        if not DB_USER or not DB_PASSWORD:
            print("\n⚠️ ERROR: No credentials provided.")
            print("You need to register at https://aact.ctti-clinicaltrials.org/ to get valid credentials.")
            print("Then run the setup_env.py script to save your credentials to the .env file.")
            return False
        
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        print("Connection successful!")
        
        # Test query - get list of tables
        with conn.cursor() as cur:
            cur.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'ctgov' ORDER BY table_name LIMIT 10"
            )
            tables = cur.fetchall()
            
            print("\nSample tables from database:")
            for i, table in enumerate(tables, 1):
                print(f"{i}. {table[0]}")
                
        conn.close()
        print("Test completed successfully.")
        return True
        
    except ImportError:
        print("Error: psycopg2 module not found. Install with: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

def test_uvx_command():
    """Test if the uvx command is available."""
    print("\nTesting uvx command...")
    try:
        result = subprocess.run(['uvx', '--version'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True,
                               check=False)
        if result.returncode == 0:
            print(f"uvx command found: {result.stdout.strip()}")
            return True
        else:
            print(f"uvx command error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running uvx command: {e}")
        return False

if __name__ == "__main__":
    print("AACT Database Connection Test")
    print("============================")
    print("This test attempts to connect directly to the AACT database.")
    print("You need personal credentials to access this database.")
    print("Register at: https://aact.ctti-clinicaltrials.org/")
    
    # Test uvx command
    uvx_result = test_uvx_command()
    
    # Test direct database connection
    db_result = test_psycopg2_connection()
    
    # Print summary
    print("\nTest Summary:")
    print(f"- uvx command: {'✅ Available' if uvx_result else '❌ Not available'}")
    print(f"- Database connection: {'✅ Successful' if db_result else '❌ Failed'}")
    
    if not db_result:
        print("\nTo set up your credentials:")
        print("1. Register at https://aact.ctti-clinicaltrials.org/")
        print("2. Run the setup script: python setup_env.py")
        print("3. Enter your AACT username and password when prompted")
        print("\nThen run this test again to verify the connection.") 