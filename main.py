from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

# Configure Gemini directly
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI(title="Blood Test Report Analyser")

def read_pdf(file_path: str) -> str:
    """Read PDF content"""
    try:
        docs = PyPDFLoader(file_path=file_path).load()
        content = ""
        for doc in docs:
            content += doc.page_content + "\n"
        return content
    except Exception as e:
        return f"Error reading PDF: {e}"

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
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Verification failed: {e}"

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
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Medical analysis failed: {e}"

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
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Nutrition analysis failed: {e}"

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
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Exercise analysis failed: {e}"

def analyze_blood_report(content: str, query: str) -> dict:
    """Comprehensive analysis using multiple specialist perspectives"""
    
    return {
        "verification": verify_document(content),
        "medical_analysis": medical_analysis(content, query),
        "nutrition_plan": nutrition_analysis(content, query),
        "exercise_plan": exercise_analysis(content, query)
    }

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
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Read PDF content
        pdf_content = read_pdf(file_path)
        
        if "Error" in pdf_content:
            raise HTTPException(status_code=400, detail=pdf_content)
        
        # Comprehensive analysis with all specialists
        analysis = analyze_blood_report(pdf_content, query)
        
        return {
            "status": "success",
            "query": query,
            "analysis": analysis,
            "file_processed": file.filename,
            "specialists_consulted": [
                "Document Verification Specialist",
                "Medical Doctor", 
                "Clinical Nutritionist",
                "Exercise Physiologist"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
