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
    python_files = [f for f in files if f.endswith(".py") or f.endswith(".js") or f.endswith(".ts") or f.endswith(".tsx") or f.endswith(".jsx") or f.endswith(".html") or f.endswith(".css") or f.endswith(".json") or f.endswith(".sh")]
    # Check if there are any Python files in the directory
    if not python_files:
        print("No Python files found in the current directory.")
        return
    # Create a README file with Gemini API
    fallback_api_urls = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}",
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    ]

    def call_gemini_api(payload):
        for url in fallback_api_urls:
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error with {url}: {response.status_code}, {response.text}")
        print("All Gemini API models failed.")
        sys.exit(1)

    with open("README.md", "w") as readme_file:
        readme_file.write("# README\n\n")
        readme_file.write("## Project Overview\n\n")
        
        # send the files list to Gemini API and get the project overview
        payload = {
            "contents": [
                {
                    "parts": [{"text": "\n".join(python_files) + "\n\nPlease provide an overview of the above files only referring to the file names. (Do not include your working process or any other information.)"}],
                }
            ]
        }

        response_content = call_gemini_api(payload)

        # Extract the overview from the response
        print("Response content:", response_content)
        overview = response_content["candidates"][0]["content"]["parts"][0]["text"]
        readme_file.write(f"{overview}\n\n")

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
                payload = {
                    "contents": [
                        {
                            "parts": [{"text": content + "\n\nPlease provide a summary of the above code."}],
                        }
                    ]
                }

                response_content = call_gemini_api(payload)

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