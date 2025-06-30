## Importing libraries and files
import os
from dotenv import load_dotenv
from crewai_tools import tool
from langchain_community.document_loaders import PDFLoader

load_dotenv()

## Creating custom pdf reader tool
@tool("BloodTestReportTool")
def read_data_tool(path: str) -> str:
    """Tool to read data from a pdf file from a path."""
    
    docs = PDFLoader(file_path=path).load()

    full_report = ""
    for data in docs:
        # Clean and format the report data
        content = data.page_content
        
        # Remove extra whitespaces and format properly
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")
            
        full_report += content + "\n"
        
    return full_report

## Creating Nutrition Analysis Tool
@tool("NutritionTool")
def nutrition_tool(blood_report_data: str) -> str:
    """Tool to analyze nutrition from blood report data."""
    # TODO: Implement nutrition analysis logic here
    return "Nutrition analysis functionality to be implemented"

## Creating Exercise Planning Tool
@tool("ExerciseTool")
def exercise_tool(blood_report_data: str) -> str:
    """Tool to create an exercise plan from blood report data."""
    # TODO: Implement exercise planning logic here
    return "Exercise planning functionality to be implemented"