# Blood Report Analysis System

A multi-agent AI system that analyzes blood test reports and provides comprehensive health insights using CrewAI and language models.

## Overview

This application uses a team of specialized AI agents to analyze uploaded blood test reports (PDF format) and provide:
- Medical assessment and interpretation
- Nutritional recommendations
- Exercise and lifestyle suggestions

## Features

- **PDF Upload Support**: Upload blood test reports in PDF format
- **Multi-Agent Analysis**: Four specialized agents work together to provide comprehensive insights
- **Streamlit Web Interface**: User-friendly interface for uploading and viewing results
- **Flexible LLM Support**: Compatible with OpenAI GPT and Google Gemini models

## Architecture

The system employs four specialized agents:

1. **Verifier Agent**: Validates the uploaded document and extracts relevant blood test data
2. **Doctor Agent**: Provides medical interpretation of test results
3. **Nutritionist Agent**: Offers dietary recommendations based on the results
4. **Exercise Specialist Agent**: Suggests fitness and lifestyle modifications

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd blood-report-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with your API key:
```env
# For OpenAI
OPENAI_API_KEY=your-api-key-here

# OR for Google Gemini
GOOGLE_API_KEY=your-api-key-here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload a blood test report PDF using the file uploader

4. Click "Process Report" to analyze the document

5. View the comprehensive analysis from all four specialists

## Project Structure

```
blood-report-analyzer/
├── main.py              # Streamlit application entry point
├── agents.py            # Agent definitions and configurations
├── tasks.py             # Task definitions for each agent
├── tools.py             # Custom tools (PDF reader)
├── .env                 # Environment variables (not tracked)
└── requirements.txt     # Python dependencies
```

## Key Components

### Agents (`agents.py`)
Defines the four specialized agents with their roles, goals, and backstories.

### Tasks (`tasks.py`)
Specifies the specific tasks each agent performs during the analysis.

### Tools (`tools.py`)
Contains the PDF reading tool that extracts text from uploaded blood reports.

### Main Application (`main.py`)
Streamlit interface that orchestrates the entire workflow.

## Recent Bug Fixes

Several critical issues were resolved to ensure proper functionality:

1. **Circular Reference Fix**: Resolved self-referential LLM initialization
2. **Tool Implementation**: Converted async class-based tool to proper function-based tool with @tool decorator
3. **Missing Imports**: Added required imports for PDF processing
4. **Agent Orchestration**: Implemented proper crew workflow using all defined agents
5. **File Path Handling**: Fixed file path passing to ensure agents can access uploaded PDFs

## Configuration

### Switching Language Models

To use OpenAI GPT:
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0.7)
```

To use Google Gemini:
```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
```

## Dependencies

- `crewai`: Multi-agent orchestration framework
- `streamlit`: Web application framework
- `langchain`: LLM integration
- `PyPDF2` or `pdfplumber`: PDF processing
- Additional dependencies listed in `requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]

## Disclaimer

This tool is for educational and informational purposes only. Always consult with qualified healthcare professionals for medical advice and interpretation of blood test results.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.
