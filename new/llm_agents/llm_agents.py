import requests
import dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.llm_model import llm_request
import logging

dotenv.load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
GPT_API_KEY = os.environ.get("GPT_API_KEY")

def get_llm_response(llm_request: llm_request):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info(f"Preparing LLM request for model: {llm_request.model_name}")

    if llm_request.model_name == "gemini":
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    else:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{llm_request.model_name}:generateContent?key={GEMINI_API_KEY}"
    logger.debug(f"Request URL: {url}")

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": llm_request.prompt
                    }
                ]
            }
        ],
    }
    logger.info(f"Sending request to LLM API with prompt: {llm_request.prompt}")

    response = requests.post(url, headers=headers, json=data)
    logger.info(f"Received response with status code: {response.status_code}")

    if response.status_code != 200:
        logger.error(f"Error: {response.status_code} - {response.text}")
        raise ValueError(f"Error: {response.status_code} - {response.text}")

    logger.debug(f"Response JSON: {response.json()}")
    return response.json()