import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.llm_model import llm_response_prompt_analysis,llm_response_feature_analysis
from models.feature_model import feature
from models.feature_model import dependency

class app:
    def __init__(self):
        self.name = ""
        self.app_type = ""
        self.tech_stack = ""
        self.features = []
        self.use_cases = []
        self.target_audience = ""
        self.description = ""
        self.other_details = ""

    def set_prompt_analysis_result(self, analysis_result: llm_response_prompt_analysis):
        self.name = analysis_result.app_name
        self.app_type = analysis_result.app_type
        self.tech_stack = analysis_result.tech_stack
        self.features = analysis_result.features
        self.use_cases = analysis_result.use_cases
        self.target_audience = analysis_result.target_audience
        self.description = analysis_result.description
        self.other_details = analysis_result.other_details

    def set_feature_analysis_result(self, analysis_result: llm_response_feature_analysis):
        self.features = analysis_result.features
        self.dependencies = analysis_result.dependencies

    def to_dict(self):
        return {
            "app_name": self.name,
            "app_type": self.app_type,
            "tech_stack": self.tech_stack,
            "features": [feat.to_dict() if isinstance(feat, feature) else feat for feat in self.features] if isinstance(self.features, list) else self.features,
            "use_cases": self.use_cases,
            "target_audience": self.target_audience,
            "description": self.description,
            "other_details": self.other_details,
            "dependencies": [dep.to_dict() if isinstance(dep, dependency) else dep for dep in self.dependencies] if hasattr(self, 'dependencies') else []
        }