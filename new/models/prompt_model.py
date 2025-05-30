import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.app import app


def prompt_analysis_prompt(prompt: str):
    return f"""
        You are an expert in analyzing software application prompts. Your task is to extract key information from the {prompt} prompt and return it in a structured JSON format.
        Your response should include the following fields:
        ```json
        {{
        "prompt_text": "<The original prompt text>",
        "app_name": "<Name of the application>",
        "app_type": "<Type of application (e.g., web, mobile, desktop)>",
        "tech_stack": "<Technology stack used>",
        "features": ["<List of features>"],
        "use_cases": ["<List of use cases>"],
        "target_audience": "<Target audience>",
        "description": "<Brief description of the application>",
        "other_details": "<Any other relevant details>"
        }}
        ```
        Make sure to provide a comprehensive analysis of the prompt, focusing on the application's purpose, its intended users, and any specific technologies or features mentioned.
        If the user doesn't mention a specific technology or feature, you can make reasonable assumptions based on common practices in the industry and fill the fields accordingly.
        Please ensure that the JSON is well-formed and includes all the required fields. If any field is not applicable or not mentioned in the prompt, you can leave it as an empty string or an empty list.
        """

def feature_analysis_prompt(app: app):
    return f"""
        You are an expert in analyzing software application features. Your task is to extract key information from the {app.name} application and return it in a structured JSON format.
        info about the application: {app.to_dict()}
        Your response should include the following fields:
        ```json
        {{
        "features": {{
            "<feature_name>": {{
                "description": "<Description of the feature>",
            }}
        }},
        "dependencies": <list of "<feature1>"|"<feature2>"|"<dependency_type_between_features>">
        }}
        ```
        For the dependencies use the same name in the feture name field.
        Please ensure that the JSON is well-formed and includes all the required fields. If any field is not applicable or not mentioned in the prompt, you can leave it as an empty string or an empty list.
        Make sure to provide a comprehensive analysis of the application's features, focusing on their purpose, functionality, and any dependencies between them.
        If the user doesn't mention a specific feature or dependency, you can make reasonable assumptions based on common practices in the industry and fill the fields accordingly.
        """
