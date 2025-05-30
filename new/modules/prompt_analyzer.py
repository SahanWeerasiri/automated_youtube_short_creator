import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.prompt_model import prompt_analysis_prompt
from llm_agents.llm_agents import get_llm_response
from models.llm_model import  llm_response_prompt_analysis, llm_request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class prompt_analyzer:
    def __init__(self, prompt: str):
        self.prompt = prompt
        logger.info("Initialized prompt_analyzer with prompt: %s", prompt[:100])

    def analyze(self):
        logger.info("Starting analysis for prompt.")
        prompt = prompt_analysis_prompt(self.prompt)
        logger.debug("Generated analysis prompt: %s", prompt)
        request = llm_request(prompt, "gemini", temperature=0.7)
        logger.debug("LLM request created: %s", request)
        response = get_llm_response(request)
        logger.info("Received response from LLM.")
        if response and "candidates" in response and len(response["candidates"]) > 0:
            text = response["candidates"][0]["content"]["parts"][0]["text"]
            logger.debug("Extracted text from response: %s", text[:100])
            result = llm_response_prompt_analysis(text)
            logger.info("Analysis complete.")
            return result
        else:
            logger.error("No valid response received from the LLM.")
            raise ValueError("No valid response received from the LLM.")
    
    def get_prompt(self):
        logger.info("Generating prompt analysis prompt.")
        return prompt_analysis_prompt(self.prompt)

if __name__ == "__main__":
    # This block is for testing the module directly
    # It can be removed or modified as needed for production use
    test_prompt = """I need to build a web application for managing personal finances. The app should use React for the frontend and Node.js for the backend.
    It should include features like budgeting, expense tracking, and financial reporting. need to save data in a real time database and should be
    accessible on both web and mobile platforms. The target audience is young professionals who want to manage their finances effectively."""
    analyzer = prompt_analyzer(test_prompt)
    analysis_result = analyzer.analyze()
    print(analysis_result)