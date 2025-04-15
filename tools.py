import os
import subprocess

def run_command(command):
    return os.system(command)

def create_file(file_path, content=""):
    with open(file_path, "w") as f:
        f.write(content)
    return f"File '{file_path}' created."

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def write_file(file_path, content):
    with open(file_path, "a") as f:
        f.write(content)
    return f"Written to '{file_path}'."

def run_git(_):
    try:
        subprocess.run(["git", "add", "."], check=True)

        result = subprocess.run(
            ["git", "commit", "-m", "Auto commit from AI assistant"],
            capture_output=True,
            text=True
        )

        if "nothing to commit" in result.stderr.lower():
            return "✅ Nothing to commit. Working tree clean."
        
        return "✅ Changes committed successfully."

    except subprocess.CalledProcessError as e:
        return f"❌ Git commit failed: {e.stderr or str(e)}"


available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Executes shell commands"
    },
    "create_file": {
        "fn": lambda x: create_file(x['file_path'], x.get('content', '')),
        "description": "Creates a file with optional content"
    },
    "read_file": {
        "fn": lambda x: read_file(x['file_path']),
        "description": "Reads content of a file"
    },
    "write_file": {
        "fn": lambda x: write_file(x['file_path'], x['content']),
        "description": "Appends content to a file"
    },
    "run_git": {
        "fn": run_git,
        "description": "Commits all changes with a default message"
    }
}
