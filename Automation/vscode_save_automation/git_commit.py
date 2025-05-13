import os
import subprocess
import sys
import dotenv
import requests

dotenv.load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def git_commit():
    # Check if the current directory is a git repository
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("This directory is not a git repository.")
        sys.exit(1)

    # Add all changes to the staging area
    subprocess.run(["git", "add", "."])

    # Check if there are any changes to commit
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], check=False)
    if result.returncode == 0:
        print("No changes to commit.")
        sys.exit(0)
    
    # Create a diff file with the changes
    with open("diff.txt", "w") as diff_file:
        subprocess.run(["git", "diff", "--cached"], stdout=diff_file)

    with open("diff.txt", "r") as diff_file:
        diff_content = diff_file.read()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [{"text": diff_content+ "\n\nPlease provide a commit message for the above changes."}],
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            sys.exit(1)

        response_content = response.json()

        # Extract the commit message from the response
        print("Response content:", response_content)
        commit_message = response_content["candidates"][0]["content"]["parts"][0]["text"]

        # Commit the changes with a message
        subprocess.run(["git", "commit", "-m", commit_message])

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    pwd = os.getcwd()
    os.chdir(directory)
    git_commit()
    # Clean up
    os.remove("diff.txt")
    os.chdir(pwd)
    print("Commit successful.")
    sys.exit(0)