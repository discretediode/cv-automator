import os
from pathlib import Path

# Change this to the actual path of your Obsidian vault
VAULT_PATH = Path("/Users/dalfin/Desktop/my_profile")

def read_vault(vault_directory):
    """
    Scans the Obsidian vault and dynamically reads ALL markdown files.
    Returns a dictionary containing the text of each file.
    """
    vault_data = {}
    
    # Check if the directory actually exists first
    if not vault_directory.exists():
        print(f"❌ Directory not found: {vault_directory}")
        return vault_data
        
    # .glob("*.md") automatically finds every Markdown file in the folder
    for file_path in vault_directory.glob("*.md"):
        filename = file_path.name  # Extracts just the file name (e.g., "skills.md")
        
        with open(file_path, "r", encoding="utf-8") as file:
            vault_data[filename] = file.read()
            print(f"✅ Successfully loaded: {filename}")
            
    return vault_data

if __name__ == "__main__":
    print("Starting Vault Indexer...\n")
    my_data = read_vault(VAULT_PATH)