import os
import subprocess
import sys
import dotenv
import requests

dotenv.load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def readme_generator():
    """Generate a README file for the project in the current directory."""
    # Check if a README file already exists
    if os.path.exists("README.md"):
        print("README.md already exists. Skipping generation.")
        return
    # Get the list of files in the current directory
    files = os.listdir(".")
    # Filter out non-Python files
    python_files = [f for f in files if f.endswith(".py") or f.endswith(".js") or f.endswith(".ts") or f.endswith(".tsx") or f.endswith(".jsx") or f.endswith(".html") or f.endswith(".css") or f.endswith(".json")]
    # Check if there are any Python files in the directory
    if not python_files:
        print("No Python files found in the current directory.")
        return
    # Create a README file with Gemini API
    with open("README.md", "w") as readme_file:
        readme_file.write("# README\n\n")
        readme_file.write("## Project Overview\n\n")
        readme_file.write("This project is a Python application.\n\n")
        readme_file.write("## Project Structure\n\n")
        readme_file.write("The project structure is as follows:\n\n")
        readme_file.write("```\n")
        for file in files:
            readme_file.write(f"- {file}\n")
        readme_file.write("```\n\n")
        readme_file.write("## Project Details\n\n")
        readme_file.write("This project contains the following files:\n\n")
        for file in python_files:
            readme_file.write(f"- {file}\n")
            with open(file, "r") as f:
                content = f.read()
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [
                        {
                            "parts": [{"text": content + "\n\nPlease provide a summary of the above code."}],
                        }
                    ]
                }

                response = requests.post(url, headers=headers, json=payload)
                if response.status_code != 200:
                    print(f"Error: {response.status_code}, {response.text}")
                    sys.exit(1)

                response_content = response.json()

                # Extract the summary from the response
                print("Response content:", response_content)
                summary = response_content["candidates"][0]["content"]["parts"][0]["text"]
                readme_file.write(f"### {file}\n")
                readme_file.write(f"{summary}\n\n")
    # Generate a diff of the changes made to the README file
    subprocess.run(["git", "add", "./README.md"], check=True)
    subprocess.run(["git", "commit", "-m", "Updated README.md"], check=True)
    

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    pwd = os.getcwd()
    os.chdir(directory)

    print(f"Generating README for {directory}...")

    # get the main file name from this directory .py/.js/...
    file_name = os.path.basename(directory)
    file_extension = os.path.splitext(file_name)[1]
    
    readme_generator()

    os.chdir(pwd)
    print("README generation successful.")
    sys.exit(0)