"""Read the .env file directly."""

import os
import pathlib

# Get the root directory
ROOT_DIR = pathlib.Path(__file__).parent.parent
ENV_PATH = ROOT_DIR / '.env'
print(f"Looking for .env file at: {ENV_PATH}")
print(f"File exists: {ENV_PATH.exists()}")

# Read the file directly
if ENV_PATH.exists():
    try:
        with open(ENV_PATH, 'r') as f:
            content = f.read()
        
        # Print content with sensitive info masked
        lines = content.splitlines()
        for line in lines:
            if line.strip() and not line.strip().startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Mask password values
                    if 'password' in key.lower() or 'secret' in key.lower() or 'key' in key.lower():
                        if value:
                            masked_value = value[:2] + '*' * (len(value) - 4) + value[-2:] if len(value) > 4 else '*' * len(value)
                            print(f"{key}={masked_value}")
                        else:
                            print(f"{key}=<empty>")
                    else:
                        print(line)
                else:
                    print(line)
    except Exception as e:
        print(f"Error reading .env file: {e}")
else:
    print("The .env file does not exist.")

# Alternative approach - try to read env vars with os.environ
print("\nEnvironment variables from os.environ:")
if 'AACT_DB_USER' in os.environ:
    print(f"AACT_DB_USER is set in os.environ")
else:
    print("AACT_DB_USER is not set in os.environ")

if 'AACT_DB_PASSWORD' in os.environ:
    print(f"AACT_DB_PASSWORD is set in os.environ")
else:
    print("AACT_DB_PASSWORD is not set in os.environ") 