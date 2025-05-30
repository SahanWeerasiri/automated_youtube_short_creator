from modules.prompt_analyzer import prompt_analyzer
from models.app import app


if __name__ == "__main__":
    # This block is for testing the module directly
    # It can be removed or modified as needed for production use
    test_prompt = """I need to build a web application for managing personal finances. The app should use React for the frontend and Node.js for the backend.
    It should include features like budgeting, expense tracking, and financial reporting. need to save data in a real time database and should be
    accessible on both web and mobile platforms. The target audience is young professionals who want to manage their finances effectively."""
    my_app = app()

    analyzer = prompt_analyzer(test_prompt)
    analysis_result = analyzer.analyze()
    my_app.set_prompt_analysis_result(analysis_result)
    analysis_result = my_app.to_dict()
    print(analysis_result)

    