import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def prompt_analysis_prompt(prompt: str):
    return f"""
        You are an expert in analyzing software application prompts. Your task is to extract key information from the {prompt} prompt and return it in a structured JSON format.
        Your response should include the following fields:
        ```json
        {{
        "prompt_text": "<The original prompt text>",
        "app_name": "<Name of the application>",
        "tech_stack": "<Technology stack used>",
        "features": ["<List of features>"],
        "use_cases": ["<List of use cases>"],
        "target_audience": "<Target audience>",
        "description": "<Brief description of the application>",
        "other_details": "<Any other relevant details>"
        }}
        ```
        Make sure to provide a comprehensive analysis of the prompt, focusing on the application's purpose, its intended users, and any specific technologies or features mentioned.
        Please ensure that the JSON is well-formed and includes all the required fields. If any field is not applicable or not mentioned in the prompt, you can leave it as an empty string or an empty list.
        """
