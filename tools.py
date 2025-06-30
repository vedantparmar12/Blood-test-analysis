import os
from dotenv import load_dotenv
from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

class BloodTestReportTool:
    @tool("read_data_tool")
    def read_data_tool(path: str) -> str:
        """
        Tool to read data from a PDF file from a path.

        Args:
            path (str): Path of the PDF file.

        Returns:
            str: Full Blood Test report file content.
        """
        if not os.path.exists(path):
            return f"Error: The file at path {path} does not exist."

        try:
            docs = PyPDFLoader(file_path=path).load()
            full_report = ""
            for data in docs:
                content = data.page_content
                # Clean and format the report data
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                full_report += content + "\n"
            return full_report
        except Exception as e:
            return f"Error reading PDF file: {e}"

# These tools are placeholders and can be implemented with actual logic.
class NutritionTool:
    @tool("analyze_nutrition_tool")
    def analyze_nutrition_tool(blood_report_data: str) -> str:
        """
        Analyzes nutrition based on blood report data.
        """
        # Placeholder for actual nutrition analysis logic
        return "Nutrition analysis functionality to be implemented"

class ExerciseTool:
    @tool("create_exercise_plan_tool")
    def create_exercise_plan_tool(blood_report_data: str) -> str:
        """
        Creates an exercise plan based on blood report data.
        """
        # Placeholder for actual exercise planning logic
        return "Exercise planning functionality to be implemented"