# Blood Test Report Analyzer 🩺

A comprehensive AI-powered system that analyzes blood test reports and provides personalized health insights, nutrition recommendations, and exercise plans using multiple specialized AI agents.

## 🚀 What's New

I recently refactored this project to fix several critical issues in the original implementation:
- **Fixed Agent Configuration**: Properly configured CrewAI agents with appropriate LLM settings
- **Improved Tool Integration**: Streamlined PDF reading tools with proper error handling
- **Enhanced Code Structure**: Separated concerns and removed problematic code patterns
- **Better Error Handling**: Added robust error handling for file operations and LLM interactions
- **Professional Agent Personas**: Replaced unprofessional agent descriptions with expert-level backgrounds

## 📋 Features

- **Multi-Agent Analysis**: Utilizes four specialized AI agents for comprehensive health analysis
- **PDF Processing**: Automatically extracts and processes blood test reports from PDF files
- **FastAPI Integration**: RESTful API endpoints for easy integration
- **Comprehensive Health Insights**: 
  - Document verification
  - Medical analysis
  - Nutrition recommendations
  - Exercise planning

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **AI Orchestration**: CrewAI
- **LLM**: Google Gemini 5.0 Flash
- **PDF Processing**: LangChain PyPDFLoader
- **Python**: 3.10+

## 📦 Installation

### Using UV (Recommended)

UV is a fast Python package installer and resolver written in Rust. It's significantly faster than pip.

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/yourusername/blood-test-analyzer.git
cd blood-test-analyzer

# Create virtual environment with UV
uv venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

### Using Traditional pip

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Configuration

1. Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

2. Ensure you have the following project structure:

```
blood-test-analyzer/
├── agents.py          # Agent definitions
├── task.py           # Task definitions
├── tools.py          # Custom tools
├── main.py           # FastAPI application
├── requirements.txt  # Dependencies
├── .env             # Environment variables
├── data/            # Directory for uploaded files
└── README.md        # This file
```

## 🚀 Running the Application

### Using UV

```bash
# Make sure virtual environment is activated
uv run python main.py
```

Or with uvicorn directly:

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Using Traditional Python

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### Health Check
```http
GET /
```

### Analyze Blood Report
```http
POST /analyze
Content-Type: multipart/form-data

Parameters:
- file: PDF file (required)
- query: Analysis query (optional, default: "Summarise my Blood Test Report")
```

Example using curl:
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@/path/to/blood_report.pdf" \
  -F "query=What are my vitamin levels?"
```

## 🤖 Agent Roles

1. **Document Verifier**: Validates that uploaded documents are blood test reports
2. **Medical Doctor**: Provides comprehensive health analysis and medical insights
3. **Clinical Nutritionist**: Creates personalized nutrition plans based on blood markers
4. **Exercise Physiologist**: Designs safe exercise programs considering health status

## 🔄 Workflow

1. User uploads a blood test report (PDF)
2. Document Verifier confirms it's a valid blood report
3. Medical Doctor analyzes the results and identifies health concerns
4. Nutritionist provides dietary recommendations
5. Exercise Specialist creates a fitness plan
6. All insights are compiled and returned to the user

## 🐛 Bug Fixes from Original Code

The original implementation had several issues that have been resolved:

- **Removed Inappropriate Content**: Eliminated unprofessional agent descriptions and behaviors
- **Fixed LLM Configuration**: Properly configured CrewAI LLM integration
- **Corrected Tool Usage**: Fixed tool decorator syntax and async handling
- **Improved Error Handling**: Added proper exception handling throughout
- **Removed Hardcoded Paths**: Made file paths dynamic and configurable
- **Fixed Memory Management**: Properly configured agent memory settings

## 📝 Requirements

Create a `requirements.txt` file:

```txt
fastapi==0.110.0
uvicorn==0.27.0
crewai==0.75.0
langchain-community==0.2.5
pypdf==4.0.0
python-dotenv==1.0.0
google-generativeai==0.3.0
python-multipart==0.0.6
```

## 🧪 Testing

You can test the API using the FastAPI automatic documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🚨 Important Notes

- Ensure your Google API key has access to Gemini models
- The application creates a temporary `data/` directory for processing files
- Uploaded files are automatically cleaned up after processing
- For production use, consider implementing authentication and rate limiting

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- CrewAI for the multi-agent framework
- Google Gemini for LLM capabilities
- FastAPI for the excellent web framework

---

**Note**: This is a demonstration project for educational purposes. Always consult with qualified healthcare professionals for medical advice.
