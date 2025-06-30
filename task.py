from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist, read_data_tool
# Creating a task to verify the blood report
verification = Task(
    description="Verify that the document at {file_path} is a blood test report. Read the document and confirm it contains blood test results.",
    expected_output="A confirmation that the document is a blood test report and a brief summary of its contents, including key blood markers found.",
    agent=verifier
)

# Creating a task for the doctor to analyze the report
help_patients = Task(
    description="Analyze the blood test report from {file_path} and provide a detailed health summary for the user's query: {query}. Focus on any abnormal values and their clinical significance.",
    expected_output="A comprehensive medical analysis of the blood test report, highlighting any abnormalities, their potential causes, and general health advice.",
    agent=doctor
)

# Creating a nutrition analysis task
nutrition_analysis = Task(
    description="Based on the blood report analysis from the previous task, provide personalized nutrition recommendations for the user's query: {query}. Consider any deficiencies or abnormal values.",
    expected_output="A detailed nutrition plan including recommended foods, supplements, and dietary changes based on the blood test results.",
    agent=nutritionist
)

# Creating an exercise planning task
exercise_planning = Task(
    description="Create a personalized exercise plan based on the health analysis from previous tasks and the user's query: {query}. Consider any health conditions or restrictions indicated by the blood work.",
    expected_output="A tailored exercise plan including types of exercises, duration, intensity, and any precautions based on the patient's health status.",
    agent=exercise_specialist
)