#!/usr/bin/env python3
"""
Updated test script for CrewAI 0.134.0
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Testing CrewAI setup...")

# Test 1: Check environment variables
print("\n1. Environment Variables:")
google_key = os.getenv('GOOGLE_API_KEY')
serper_key = os.getenv('SERPER_API_KEY')
print(f"   GOOGLE_API_KEY: {'✅ Set' if google_key else '❌ Missing'}")
print(f"   SERPER_API_KEY: {'✅ Set' if serper_key else '❌ Missing'}")

# Test 2: Import dependencies
print("\n2. Testing imports:")
try:
    import crewai
    print(f"   CrewAI: ✅ {crewai.__version__}")
except Exception as e:
    print(f"   CrewAI: ❌ {e}")
    sys.exit(1)

try:
    from langchain_community.document_loaders import PyPDFLoader
    print("   PyPDFLoader: ✅")
except Exception as e:
    print(f"   PyPDFLoader: ❌ {e}")

# Test 3: Test LLM configuration
print("\n3. Testing LLM configuration:")
try:
    from crewai import LLM
    
    # Try to create LLM with Google API
    llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    print("   LLM creation: ✅")
    
except Exception as e:
    print(f"   LLM creation: ❌ {e}")
    print("   Trying alternative LLM setup...")
    
    try:
        # Alternative setup
        os.environ["OPENAI_API_BASE"] = "https://generativelanguage.googleapis.com/v1beta"
        os.environ["OPENAI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
        
        llm = LLM(model="gpt-3.5-turbo")  # This will actually use Gemini
        print("   Alternative LLM: ✅")
    except Exception as e2:
        print(f"   Alternative LLM: ❌ {e2}")
        llm = None

# Test 4: Create basic agent
print("\n4. Testing agent creation:")
try:
    from crewai import Agent
    
    if llm:
        test_agent = Agent(
            role="Test Agent",
            goal="Test if agent creation works",
            backstory="A simple test agent",
            verbose=False,
            allow_delegation=False,
            llm=llm
        )
    else:
        test_agent = Agent(
            role="Test Agent",
            goal="Test if agent creation works", 
            backstory="A simple test agent",
            verbose=False,
            allow_delegation=False
        )
    print("   Agent creation: ✅")
    
except Exception as e:
    print(f"   Agent creation: ❌ {e}")
    import traceback
    print(f"   Error details: {traceback.format_exc()}")

# Test 5: Test tool creation (updated for new CrewAI)
print("\n5. Testing tool creation:")
try:
    from crewai_tools import tool
    
    @tool
    def test_tool(input_text: str) -> str:
        """A simple test tool"""
        return f"Tool received: {input_text}"
    
    print("   Tool creation: ✅")
    
    # Test tool execution
    try:
        result = test_tool.run("hello")
        print(f"   Tool execution: ✅ {result}")
    except Exception as e:
        print(f"   Tool execution: ❌ {e}")
    
except ImportError:
    print("   crewai_tools not available, trying crewai.tools...")
    try:
        from crewai.tools import tool
        
        @tool
        def test_tool(input_text: str) -> str:
            """A simple test tool"""
            return f"Tool received: {input_text}"
        
        print("   Tool creation (crewai.tools): ✅")
        
    except Exception as e:
        print(f"   Tool creation: ❌ {e}")

# Test 6: Test basic crew
print("\n6. Testing basic crew:")
try:
    from crewai import Crew, Task, Process
    
    # Create minimal task
    test_task = Task(
        description="Say hello world",
        expected_output="A simple hello world message",
        agent=test_agent
    )
    
    # Create minimal crew
    test_crew = Crew(
        agents=[test_agent],
        tasks=[test_task],
        process=Process.sequential,
        verbose=True
    )
    
    print("   Crew creation: ✅")
    
    # Try to run the crew
    print("   Testing crew execution...")
    try:
        result = test_crew.kickoff()
        print(f"   Crew execution: ✅")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Crew execution: ❌ {e}")
        import traceback
        print(f"   Full error: {traceback.format_exc()}")
    
except Exception as e:
    print(f"   Crew setup: ❌ {e}")
    import traceback
    print(f"   Error details: {traceback.format_exc()}")

print("\n🎉 Testing complete!")
print("\nNext steps based on results:")
print("- If LLM creation failed, you need to set up the API properly")
print("- If tool creation failed, we need to use the correct import")
print("- If crew execution failed, there might be an API configuration issue")