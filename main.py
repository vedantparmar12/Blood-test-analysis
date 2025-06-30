import uvicorn
import asyncio
import sys
import os
import uuid
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from celery import Celery
from sqlalchemy import create_engine, Column, String, Text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from .env file
load_dotenv()

# Configure Gemini directly using the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize FastAPI app
app = FastAPI(title="Blood Test Report Analyser")

# Celery configuration
celery = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./analysis_results.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the database model for storing analysis results
class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(String, primary_key=True, index=True)
    query = Column(String)
    verification = Column(Text)
    medical_analysis = Column(Text)
    nutrition_plan = Column(Text)
    exercise_plan = Column(Text)

# Create the database table if it doesn't exist
if not inspect(engine).has_table("analysis_results"):
    Base.metadata.create_all(bind=engine)


def read_pdf(file_path: str) -> str:
    """Read PDF content"""
    docs = PyPDFLoader(file_path=file_path).load()
    content = ""
    for doc in docs:
        content += doc.page_content + "\n"
    return content

def verify_document(content: str) -> str:
    """Verify if document is a blood test report"""
    prompt = f"""
    As a Document Verification Specialist, analyze this document and confirm if it's a valid blood test report.
    
    Document Content:
    {content}
    
    Provide:
    1. Confirmation if this is a blood test report
    2. Laboratory name and key identifiers
    3. List of main blood markers/tests included
    4. Overall document quality assessment
    """
    response = model.generate_content(prompt)
    return response.text

def medical_analysis(content: str, query: str) -> str:
    """Medical doctor analysis"""
    prompt = f"""
    As an experienced Medical Doctor, analyze this blood test report and provide comprehensive medical insights.
    
    Blood Test Report:
    {content}
    
    User Query: {query}
    
    Provide detailed medical analysis focusing on:
    1. Abnormal values and their clinical significance
    2. Potential health concerns or conditions indicated
    3. Immediate medical recommendations
    4. Follow-up tests or consultations needed
    5. Overall health assessment
    
    Be thorough but include appropriate medical disclaimers.
    """
    response = model.generate_content(prompt)
    return response.text

def nutrition_analysis(content: str, query: str) -> str:
    """Clinical nutritionist analysis"""
    prompt = f"""
    As a Clinical Nutritionist, analyze this blood test report and provide detailed nutrition recommendations.
    
    Blood Test Report:
    {content}
    
    User Query: {query}
    
    Provide comprehensive nutrition plan including:
    1. Specific foods to include based on blood markers
    2. Foods to avoid or limit
    3. Supplement recommendations if indicated
    4. Meal timing and portion guidance
    5. Specific dietary modifications for any abnormal values
    6. Sample meal plans or food combinations
    7. Hydration recommendations
    
    Be specific and actionable.
    """
    response = model.generate_content(prompt)
    return response.text

def exercise_analysis(content: str, query: str) -> str:
    """Exercise physiologist analysis"""
    prompt = f"""
    As an Exercise Physiologist, analyze this blood test report and create a tailored exercise program.
    
    Blood Test Report:
    {content}
    
    User Query: {query}
    
    Provide detailed exercise plan including:
    1. Recommended types of exercise based on health status
    2. Frequency, intensity, and duration guidelines
    3. Exercise precautions based on blood markers
    4. Progressive workout plan for beginners to advanced
    5. Specific exercises for any health concerns identified
    6. Recovery and rest recommendations
    7. Monitoring guidelines during exercise
    
    Consider any contraindications from the blood work.
    """
    response = model.generate_content(prompt)
    return response.text


@celery.task(bind=True)
def analyze_blood_report_task(self, file_path: str, query: str):
    """Celery task for comprehensive analysis that uses its own ID for the DB."""
    pdf_content = read_pdf(file_path)
    if "Error" in pdf_content:
        # Handle error appropriately
        return {"error": pdf_content}
    
    analysis = {
        "verification": verify_document(pdf_content),
        "medical_analysis": medical_analysis(pdf_content, query),
        "nutrition_plan": nutrition_analysis(pdf_content, query),
        "exercise_plan": exercise_analysis(pdf_content, query)

    }
    
    # Store result in database
    db = SessionLocal()
    # Use the Celery task's own ID as the primary key
    db_result = AnalysisResult(
        id=self.request.id,
        query=query,
        **analysis
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    db.close()
    
    # Clean up the file after processing
    if os.path.exists(file_path):
        os.remove(file_path)
        
    return {"status": "success", "result_id": self.request.id}

@app.get("/")
async def root():
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    os.makedirs("data", exist_ok=True)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    

    task = analyze_blood_report_task.delay(file_path, query)
    
    return {
        "status": "processing",
        "task_id": task.id,
        "message": "Your request is being processed. Use the task_id to check the status."
    }

@app.get("/results/{task_id}")
async def get_analysis_result(task_id: str):
    db = SessionLocal()
    result = db.query(AnalysisResult).filter(AnalysisResult.id == task_id).first()
    db.close()
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found. The task may still be processing or it failed.")
    return result

async def main():
    """Run the server with proper async handling"""
    config = uvicorn.Config(
        "__main__:app",

        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    if sys.platform == "win32" and sys.version_info >= (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

