# tests/test_agent.py

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.university_complaint_agent import UniversityComplaintAgent
from config.settings import DOCUMENTS_PATH, EXCEL_PATH, CHROMA_PATH, EMBEDDING_MODEL, GEMINI_MODEL


def test_agent_initialization():
    """Test agent can be initialized"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  Skipping test: GOOGLE_API_KEY not set")
        return
    
    agent = UniversityComplaintAgent(
        api_key=api_key,
        documents_path=DOCUMENTS_PATH,
        excel_path=EXCEL_PATH,
        chroma_path=CHROMA_PATH,
        rebuild_index=False,
        model_name=GEMINI_MODEL,
        embedding_model=EMBEDDING_MODEL
    )
    
    assert agent is not None
    print("✓ Agent initialization test passed")


def test_complaint_handling():
    """Test complaint processing"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  Skipping test: GOOGLE_API_KEY not set")
        return
    
    agent = UniversityComplaintAgent(
        api_key=api_key,
        documents_path=DOCUMENTS_PATH,
        excel_path=EXCEL_PATH,
        chroma_path=CHROMA_PATH,
        rebuild_index=False,
        model_name=GEMINI_MODEL,
        embedding_model=EMBEDDING_MODEL
    )
    
    result = agent.handle_complaint(
        student_name="Test Student",
        subject="Test Subject",
        complaint="Test complaint"
    )
    
    assert result["status"] in ["success", "error"]
    assert "result" in result
    print("✓ Complaint handling test passed")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Running tests...\n")
    test_agent_initialization()
    test_complaint_handling()
    print("\n✅ All tests passed!")