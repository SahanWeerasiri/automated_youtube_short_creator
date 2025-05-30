import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class llm_request:
    def __init__(self, prompt: str, model_name: str, temperature: float = 0.7):
        self.prompt = prompt
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = 0.9
        self.top_k = 40
        self.max_tokens = 1024
        self.max_output_tokens = 1024
        self.stop_sequences = []
        self.return_likelihoods = "NONE"
        self.response_format = "json"

class llm_response_prompt_analysis:
    def __init__(self, text: str):
        print("Parsing LLM response for prompt analysis...")
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        text = json.loads(text)
        self.app_name = text.get("app_name", "")
        self.tech_stack = text.get("tech_stack", "")
        self.features = text.get("features", [])
        self.use_cases = text.get("use_cases", [])
        self.target_audience = text.get("target_audience", "")
        self.description = text.get("description", "")
        self.other_details = text.get("other_details", "")
