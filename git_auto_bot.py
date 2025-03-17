import os
import shutil
import subprocess
from datetime import datetime

# Configuration
REPO_DIR = r"C:\Users\ritik\Desktop\geeks\Black-Friday\DS-projects"  # Path to your local repository
FOLDER_PATH = r"C:\Users\ritik\Desktop\geeks\Black-Friday\DS-projects"  # Path to the folder containing files
COMMIT_MESSAGE = "Repo Updated"
UPLOADED_FILES_LOG = "uploaded_files.txt"  # File to track uploaded files
REMOTE_URL = "https://github.com/vritik907/Heart-Disease-EDA.git"  # Remote repository URL
MOVE_DIR = r"C:\Users\ritik\Desktop\geeks\Black-Friday\Heart-deasese\uploded"  # Folder to move uploaded files

def load_uploaded_files():
    """Load the list of already uploaded files."""
    if not os.path.exists(UPLOADED_FILES_LOG):
        return set()
    with open(UPLOADED_FILES_LOG, "r") as f:
        return set(f.read().splitlines())

def save_uploaded_file(file_name):
    """Save the name of the uploaded file to the log."""
    with open(UPLOADED_FILES_LOG, "a") as f:
        f.write(file_name + "\n")

def setup_remote():
    """Ensure the remote repository is set up correctly."""
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
        if REMOTE_URL not in result.stdout.strip():
            print("Updating remote repository URL...")
            subprocess.run(["git", "remote", "set-url", "origin", REMOTE_URL], check=True)
    except subprocess.CalledProcessError:
        print("Setting up remote repository...")
        subprocess.run(["git", "remote", "add", "origin", REMOTE_URL], check=True)
        print("Remote repository set up successfully.")

def git_add_commit_push(file_name):
    """Add, commit, and push a file to GitHub, then move it."""
    try:
        # Change to the repository directory
        os.chdir(REPO_DIR)

        # Check if the file has been modified
        result = subprocess.run(["git", "status", "--porcelain", file_name], capture_output=True, text=True)
        if not result.stdout.strip():  # No changes detected
            print(f"No changes detected for {file_name}. Skipping.")
            return

        # Git add the specific file
        print(f"Staging {file_name}...")
        subprocess.run(["git", "add", file_name], check=True)

        # Git commit with a timestamped message
        commit_message = f"{COMMIT_MESSAGE} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"Committing {file_name} with message: {commit_message}")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Git push to the remote repository
        print(f"Pushing {file_name} to GitHub...")
        subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)

        # Mark the file as uploaded
        save_uploaded_file(file_name)
        print(f"Successfully pushed {file_name} to GitHub.")

        # Move the file after successful upload
        file_path = os.path.join(FOLDER_PATH, file_name)
        if not os.path.exists(MOVE_DIR):
            os.makedirs(MOVE_DIR)  # Create destination folder if it doesn't exist
        shutil.move(file_path, os.path.join(MOVE_DIR, file_name))
        print(f"Moved {file_name} to {MOVE_DIR}.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while processing {file_name}: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")

def upload_one_file():
    """Finds and uploads one file at a time."""
    files = [f for f in os.listdir(FOLDER_PATH) if os.path.isfile(os.path.join(FOLDER_PATH, f))]

    if not files:
        print("No files found in the folder.")
        return

    uploaded_files = load_uploaded_files()

    # Find the first file that hasn't been uploaded
    for file_name in files:
        if file_name not in uploaded_files:
            file_path = os.path.join(FOLDER_PATH, file_name)
            setup_remote()  # Ensure the remote is set up
            git_add_commit_push(file_path)
            break  # Upload only one file per run
    else:
        print("All files have already been uploaded.")

if __name__ == "__main__":
    upload_one_file()
