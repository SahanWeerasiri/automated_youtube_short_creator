import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.prompt_model import feature_analysis_prompt
from llm_agents.llm_agents import get_llm_response
from models.llm_model import  llm_response_feature_analysis, llm_request
from models.app import app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class feature_analyzer:
    def __init__(self, app: app):
        self.app = app
        logger.info("Initialized feature_analyzer with app: %s", app.name)

    def analyze(self):
        logger.info("Starting analysis for features.")
        prompt = feature_analysis_prompt(self.app)
        logger.debug("Generated analysis prompt: %s", prompt)
        request = llm_request(prompt, "gemini", temperature=0.7)
        logger.debug("LLM request created: %s", request)
        response = get_llm_response(request)
        logger.info("Received response from LLM.")
        if response and "candidates" in response and len(response["candidates"]) > 0:
            text = response["candidates"][0]["content"]["parts"][0]["text"]
            logger.debug("Extracted text from response: %s", text[:100])
            result = llm_response_feature_analysis(text)
            logger.info("Analysis complete.")
            return result
        else:
            logger.error("No valid response received from the LLM.")
            raise ValueError("No valid response received from the LLM.")
    
    def get_prompt(self):
        logger.info("Generating feature analysis prompt.")
        return feature_analysis_prompt(self.app)

if __name__ == "__main__":
    from models.feature_model import feature
    # This block is for testing the module directly
    # It can be removed or modified as needed for production use
    test_app = app()
    test_app.set_prompt_analysis_result(analysis_result={
        "prompt_text": "I need to build a web application for managing personal finances. The app should use React for the frontend and Node.js for the backend.",
        "name": "Personal Finance Manager",
        "description": "A web application for managing personal finances.",
        "app_type": "web",
        "tech_stack": "React, Node.js",
        "features": [
            "Budgeting",
            "Expense Tracking",
            "Financial Reporting"
        ],
        "use_cases": [
            "Track monthly expenses",
            "Create budgets",
            "Generate financial reports"
        ],
        "target_audience": "Young professionals",
        "other_details": "Should be accessible on both web and mobile platforms."
    }
    )
    analyzer = feature_analyzer(test_app)
    analysis_result = analyzer.analyze()
    print(analysis_result)