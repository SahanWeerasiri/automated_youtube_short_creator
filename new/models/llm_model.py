import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.feature_model import feature, dependency

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
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        text = json.loads(text)
        self.app_name = text.get("app_name", "")
        self.app_type = text.get("app_type", "")
        self.tech_stack = text.get("tech_stack", "")
        self.features = text.get("features", [])
        self.use_cases = text.get("use_cases", [])
        self.target_audience = text.get("target_audience", "")
        self.description = text.get("description", "")
        self.other_details = text.get("other_details", "")

class llm_response_feature_analysis:
    def __init__(self, text: str):
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        print(text)
        text = json.loads(text)
        # Parse features
        # Parse features
        self.features = {}
        self.feature_objects = {}
        features_dict = text.get("features", {})
        for fname, fdata in features_dict.items():
            desc = fdata.get("description", "")
            feat_obj = feature(name=fname, description=desc)
            self.features[fname] = {
            "description": desc
            }
            self.feature_objects[fname] = feat_obj

        # Parse dependencies
        self.dependencies = []
        self.dependency_objects = []
        dependencies_str = text.get("dependencies", "")
        if dependencies_str:
            dep_list = dependencies_str
            for dep in dep_list:
                parts = dep
                if len(parts) == 3:
                    feature1, dep_type, feature2 = parts
                    feature1 = self.feature_objects.get(feature1.strip())
                    feature2 = self.feature_objects.get(feature2.strip())
                    dep_type = dep_type.strip()
                    self.dependencies.append({
                        "feature1": feature1,
                        "dependency_type": dep_type,
                        "feature2": feature2
                    })
                    # Build dependency object if features exist
                    f1_obj = feature1
                    f2_obj = feature2
                    if f1_obj and f2_obj:
                        dep_obj = dependency(feature1=f1_obj, feature2=f2_obj, dependency_type=dep_type)
                        self.dependency_objects.append(dep_obj)
