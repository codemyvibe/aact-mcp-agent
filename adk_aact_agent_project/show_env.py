"""Show environment variables loaded from .env file."""

import os
import pathlib
from dotenv import load_dotenv
import sys

# Get the root directory
ROOT_DIR = pathlib.Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / '.env'
print(f"Looking for .env file at: {ENV_PATH}")
print(f"File exists: {ENV_PATH.exists()}")

# Load environment variables
load_dotenv(ENV_PATH)

# Print the loaded variables (mask sensitive info)
def mask_value(value):
    """Mask sensitive values for display."""
    if not value:
        return "<empty>"
    if len(value) <= 4:
        return "*" * len(value)
    return value[:2] + "*" * (len(value) - 4) + value[-2:]

# Print the environment variables we're looking for
print("\nLoaded environment variables:")
print(f"AACT_DB_USER: {os.getenv('AACT_DB_USER', '<not set>')} (masked: {mask_value(os.getenv('AACT_DB_USER', ''))})")
print(f"AACT_DB_PASSWORD: {'<set>' if os.getenv('AACT_DB_PASSWORD') else '<not set>'} (masked: {mask_value(os.getenv('AACT_DB_PASSWORD', ''))})")

# Print what the MCP server will receive
print("\nValues that will be passed to MCP server:")
print(f"DB_USER: {os.getenv('AACT_DB_USER', '<not set>')}")
print(f"DB_PASSWORD: {'<set>' if os.getenv('AACT_DB_PASSWORD') else '<not set>'}")

# Print Python info
print("\nPython info:")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

if __name__ == "__main__":
    print("\nThis script displays the environment variables loaded from the .env file.")
    print("If credentials are shown as <not set>, verify that the .env file exists and contains the correct values.") 