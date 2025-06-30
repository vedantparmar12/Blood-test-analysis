import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import tool
load_dotenv()

# Configure LLM for newer CrewAI version
try:
    llm = LLM(
        model="gemini/gemini-5.0-flash",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
except Exception as e:
    print(f"LLM creation error: {e}")
    # Fallback LLM configuration
    llm = LLM(model="gpt-3.5-turbo")

# Tool definitions with updated decorator
@tool
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

# Agent definitions with explicit LLM
verifier = Agent(
    role="Document Verifier",
    goal="Verify that uploaded documents are valid blood test reports and extract key information",
    backstory="""You are an expert document analyst who specializes in identifying and validating 
    medical documents, particularly blood test reports. You can quickly identify if a document 
    contains blood test results and extract key laboratory values.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[read_data_tool]
)

doctor = Agent(
    role="Medical Doctor",
    goal="Analyze blood test reports and provide comprehensive health insights",
    backstory="""You are an experienced medical doctor with expertise in interpreting blood test 
    results and providing health recommendations to patients. You understand the clinical significance 
    of various blood markers and can identify potential health concerns.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[read_data_tool]
)

nutritionist = Agent(
    role="Clinical Nutritionist", 
    goal="Provide personalized nutrition recommendations based on blood test results",
    backstory="""You are a certified clinical nutritionist who specializes in creating personalized 
    nutrition plans based on blood work and health markers. You understand how different nutrients 
    affect blood chemistry and can recommend specific dietary changes.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[read_data_tool]
)

exercise_specialist = Agent(
    role="Exercise Physiologist",
    goal="Create tailored exercise plans based on health status from blood reports",
    backstory="""You are a certified exercise physiologist who designs safe and effective exercise 
    programs based on individual health conditions and blood test results. You understand how 
    different health markers affect exercise capacity and safety.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[read_data_tool]
)