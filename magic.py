import os
import subprocess
import sys
import json
import requests
import shutil
from datetime import datetime

# File Paths
CREDENTIALS_FILE = os.path.expanduser("~/.github_credentials.json")
BASE_DIR = os.getcwd()

# Execute command with error handling
def execute_command(command, error_message):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{error_message}\n{e.stderr}")
        sys.exit(1)

# Load credentials from the local file
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as cred_file:
            return json.load(cred_file)
    return None

# Save credentials securely
def save_credentials(username, token):
    creds = {
        "username": username,
        "token": token
    }
    with open(CREDENTIALS_FILE, "w") as cred_file:
        json.dump(creds, cred_file)
    print(f"Credentials saved to {CREDENTIALS_FILE}")

# Authenticate via Personal Access Token and save for later use
def authenticate():
    print("Authenticating with GitHub...")
    username = input("Enter your GitHub username: ").strip()
    token = input("Enter your GitHub Personal Access Token (PAT): ").strip()
    save_credentials(username, token)
    return username, token

# Create a directory structure with organized folders
def create_folder_structure():
    folder_names = [
        "payloads-repository", "payloads-repository/xss", "payloads-repository/csrf",
        "payloads-repository/command_injection", "payloads-repository/clickjacking",
        "payloads-repository/ssti", "payloads-repository/ldap_injection", 
        "cheatsheets", "cheatsheets/exploits", "logs"
    ]
    for folder in folder_names:
        path = os.path.join(BASE_DIR, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created folder: {path}")

# Create sample payload files
def create_payload_files():
    payload_data = {
        "xss/xss_payloads.txt": ["<script>alert('XSS');</script>"],
        "csrf/csrf_payloads.html": ["<form action='http://malicious.com' method='post'> ... </form>"],
        "command_injection/linux_command_injection.txt": ["; rm -rf /", "&& cat /etc/passwd"],
        "clickjacking/clickjack_payload.html": ["<iframe src='http://target.com'></iframe>"],
        "ssti/jinja2_ssti_payloads.txt": ["{{7*7}}"],
        "ldap_injection/basic_ldap_injection.txt": ["(cn=*))(|(cn=*)"]
    }
    for filename, content in payload_data.items():
        path = os.path.join(BASE_DIR, "payloads-repository", filename)
        with open(path, "w") as file:
            file.write("\n".join(content))
            print(f"Created payload file: {path}")

# Get repositories list
def get_repositories(username, token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve repositories. Please check your credentials.")
        sys.exit(1)

# Create a new repository on GitHub
def create_new_repository(username, token):
    repo_name = input("Enter a new name for the GitHub repository: ").strip()
    description = input("Enter a description for the repository: ").strip()
    is_private = input("Should the repository be private? (y/n): ").strip().lower() in ['y', 'yes']

    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {token}"}
    data = {
        "name": repo_name,
        "description": description,
        "private": is_private
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully.")
        return response.json()
    else:
        print(f"Failed to create repository: {response.json()['message']}")
        sys.exit(1)

# Set up GitHub remote URL
def setup_github_remote(url):
    print("Setting up GitHub remote URL...")
    try:
        execute_command(f"git remote add origin {url}", "Failed to set Git remote URL.")
    except SystemExit:
        print("Remote origin already exists. Replacing with new URL...")
        execute_command(f"git remote set-url origin {url}", "Failed to update Git remote URL.")

# Create a GitHub webhook
def create_webhook(repo_full_name, token):
    print("Creating a webhook for the repository...")
    url = f"https://api.github.com/repos/{repo_full_name}/hooks"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": "web",
        "active": True,
        "events": ["push", "pull_request"],
        "config": {
            "url": "https://your-webhook-url.com/",
            "content_type": "json"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Webhook created successfully.")
    else:
        print(f"Failed to create webhook: {response.json()['message']}")
        sys.exit(1)

# Log activity
def log_activity(message):
    log_file = os.path.join(BASE_DIR, "logs", f"{datetime.now().date()}.log")
    with open(log_file, "a") as file:
        file.write(f"{datetime.now()} - {message}\n")

# Main function
def main():
    print("Welcome to the GitHub Repository Setup Automation Script.")

    # Load or authenticate credentials
    creds = load_credentials()
    if creds:
        print(f"Using saved credentials for {creds['username']}.")
        username, token = creds['username'], creds['token']
    else:
        username, token = authenticate()

    # Folder structure setup
    create_folder_structure()
    create_payload_files()
    
    # Ask if user wants to create a new repository or select an existing one
    new_repo = input("Do you want to create a new repository? [Y/n]: ").strip().lower() in ["y", "yes", ""]
    if new_repo:
        repo_info = create_new_repository(username, token)
    else:
        repositories = get_repositories(username, token)
        for i, repo in enumerate(repositories):
            print(f"{i + 1}. {repo['name']}")
        choice = int(input("Enter the number of the repository you want to work with: ")) - 1
        if choice < 0 or choice >= len(repositories):
            print("Invalid choice. Exiting...")
            sys.exit(1)
        repo_info = repositories[choice]

    # Set up GitHub remote and deploy key if needed
    github_url = repo_info["clone_url"].replace("https://", f"https://{username}:{token}@")
    setup_github_remote(github_url)

    # Set up Git branch
    print("Renaming branch to main...")
    execute_command("git branch -M main", "Failed to rename branch to main.")

    # Commit and push changes
    print("Adding all changes...")
    execute_command("git add .", "Failed to add changes.")
    execute_command('git commit -m "Initial commit"', "Failed to commit changes.")
    print("Pushing changes to GitHub...")
    execute_command("git push -u origin main", "Failed to push changes to GitHub.")

    # Create webhook for repository
    create_webhook(repo_info["full_name"], token)

    print("Repository setup and push completed successfully!")
    log_activity("Repository setup and push completed successfully.")

if __name__ == "__main__":
    main()
