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

    def set_prompt_analysis_result(self, analysis_result: dict):
        self.name = analysis_result.get("app_name", "")
        self.app_type = analysis_result.get("app_type", "")
        self.tech_stack = analysis_result.get("tech_stack", "")
        self.features = analysis_result.get("features", [])
        self.use_cases = analysis_result.get("use_cases", [])
        self.target_audience = analysis_result.get("target_audience", "")
        self.description = analysis_result.get("description", "")
        self.other_details = analysis_result.get("other_details", "")

    def to_dict(self):
        return {
            "app_name": self.name,
            "app_type": self.app_type,
            "tech_stack": self.tech_stack,
            "features": self.features,
            "use_cases": self.use_cases,
            "target_audience": self.target_audience,
            "description": self.description,
            "other_details": self.other_details
        }