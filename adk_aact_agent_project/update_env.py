"""Update .env file with AACT database credentials.

Replace the placeholders below with your actual AACT credentials
before running this script.
"""

import os
import pathlib

# IMPORTANT: Replace these with your actual AACT credentials
DB_USER = "your_username_here"  # Replace with your AACT username
DB_PASSWORD = "your_password_here"  # Replace with your AACT password

# Get the root directory
ROOT_DIR = pathlib.Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / '.env'
print(f"Target .env file: {ENV_PATH}")

# Check if .env file exists
if ENV_PATH.exists():
    print(f"The .env file exists.")
    # Read existing content
    with open(ENV_PATH, 'r') as f:
        existing_content = f.read()
else:
    print(f"The .env file does not exist. It will be created.")
    existing_content = ""

# Check if credentials have been updated
if DB_USER == "your_username_here" or DB_PASSWORD == "your_password_here":
    print("\nERROR: Please edit this script and replace the placeholders with your actual credentials.")
    print("Open update_env.py in a text editor and modify lines 11-12.")
    exit(1)

# Parse existing file into key-value pairs
env_data = {}
for line in existing_content.splitlines():
    line = line.strip()
    if not line or line.startswith('#'):
        continue
        
    if '=' in line:
        key, value = line.split('=', 1)
        env_data[key.strip()] = value.strip()

# Add or update credentials
env_data['AACT_DB_USER'] = DB_USER
env_data['AACT_DB_PASSWORD'] = DB_PASSWORD

# Write updated content back to file
with open(ENV_PATH, 'w') as f:
    for key, value in env_data.items():
        f.write(f"{key}={value}\n")

print("\nCredentials have been added to .env file:")
for key in env_data:
    if key.lower().endswith(('password', 'key', 'secret')):
        masked = "*" * len(env_data[key])
        print(f"  {key}={masked}")
    else:
        print(f"  {key}={env_data[key]}")

print("\nRun test_direct_connection.py to verify database access.") 