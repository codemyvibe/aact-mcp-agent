"""Add credentials to .env file without overwriting existing values."""

import os
import pathlib

# Get the root directory
ROOT_DIR = pathlib.Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / '.env'
print(f"Target .env file: {ENV_PATH}")

# Check if file exists
if ENV_PATH.exists():
    print(f"The .env file exists.")
    # Read existing content
    with open(ENV_PATH, 'r') as f:
        existing_content = f.read()
else:
    print(f"The .env file does not exist. It will be created.")
    existing_content = ""

# Get credentials
print("\nPlease enter your AACT database credentials:")
db_user = input("AACT_DB_USER: ")
db_password = input("AACT_DB_PASSWORD: ")

if not db_user or not db_password:
    print("Error: Both username and password are required.")
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
env_data['AACT_DB_USER'] = db_user
env_data['AACT_DB_PASSWORD'] = db_password

# Write updated content back to file
with open(ENV_PATH, 'w') as f:
    for key, value in env_data.items():
        f.write(f"{key}={value}\n")

print("\nCredentials have been added to .env file.")
print(f"Environment variables in .env file:")
for key in env_data:
    if key.lower().endswith(('password', 'key', 'secret')):
        print(f"  {key}=********")
    else:
        print(f"  {key}={env_data[key]}")

print("\nRun test_direct_connection.py to verify database access.") 