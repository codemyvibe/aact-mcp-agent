"""Setup environment variables for the AACT Query Agent.

This script helps you set up the required environment variables
for accessing the AACT database.
"""

import os
import pathlib
import sys

def main():
    """Set up the environment variables."""
    # Get the root directory
    root_dir = pathlib.Path(__file__).parent.parent
    env_path = root_dir / '.env'
    
    print("AACT Database Credentials Setup")
    print("===============================")
    print(f"This will update the .env file at: {env_path}")
    
    if env_path.exists():
        print(f"\nThe .env file exists. Current contents:")
        with open(env_path, 'r') as f:
            content = f.read()
            
            # Display content with sensitive info masked
            for line in content.splitlines():
                if '=' in line and ('password' in line.lower() or 'key' in line.lower() or 'secret' in line.lower()):
                    key, value = line.split('=', 1)
                    if value:
                        masked = value[:2] + '*' * (len(value) - 4) + value[-2:] if len(value) > 4 else '*' * len(value)
                        print(f"{key}={masked}")
                    else:
                        print(f"{key}=<empty>")
                else:
                    print(line)
    else:
        print("\nThe .env file does not exist yet. It will be created.")
    
    print("\nPlease enter your AACT database credentials:")
    print("(You need to register at https://aact.ctti-clinicaltrials.org/)")
    
    username = input("AACT Database Username: ")
    password = input("AACT Database Password: ")
    
    if not username or not password:
        print("\nError: Username and password cannot be empty.")
        return
    
    # Read existing content if file exists
    existing_content = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    existing_content[key.strip()] = value.strip()
    
    # Update credentials
    existing_content['AACT_DB_USER'] = username
    existing_content['AACT_DB_PASSWORD'] = password
    
    # Write back to file
    with open(env_path, 'w') as f:
        for key, value in existing_content.items():
            f.write(f"{key}={value}\n")
    
    print("\nCredentials have been saved to .env file.")
    print("You can now run the agent or test scripts.")

if __name__ == "__main__":
    main() 