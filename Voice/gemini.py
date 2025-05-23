import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def summarize_text(text):
    prompt = (
        f"Summarize the following text and point out the important events:\n\n{text}\n\nNote:just give me the summary and remove markdowns"
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.ok:
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "No summary found in response."
    else:
        print(f"Error: {response.status_code} {response.text}")
        return "Error in API request."

# Example usage:
if __name__ == "__main__":
    text = "OpenAI released ChatGPT, which quickly became popular for its conversational abilities. Later, plugins and API access were introduced, expanding its use cases."
    summary = summarize_text(text)
    print(summary)