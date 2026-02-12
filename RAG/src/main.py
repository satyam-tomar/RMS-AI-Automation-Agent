# src/main.py

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from src.agents.university_complaint_agent import UniversityComplaintAgent
from config.settings import (
    DOCUMENTS_PATH,
    EXCEL_PATH,
    CHROMA_PATH,
    EMBEDDING_MODEL,
    GEMINI_MODEL
)


def check_pdf_documents():
    rules_dir = Path(DOCUMENTS_PATH) 
    pdf_files = list(rules_dir.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF documents found in {rules_dir}. "
            "Please add your university policy PDFs."
        )

    print(f"✓ Found {len(pdf_files)} PDF documents in university_rules/:")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")


def run_tests(agent):
    print("\n" + "="*80)
    print("TESTING COMPLAINTS")
    print("="*80)
    
    tests = [
        {
            "subject": "Attendance Shortage",
            "complaint": "I have 68% attendance due to hospitalization for 10 days. Have medical certificates. Can I take exams?"
        },
        {
            "subject": "Grade Re-evaluation",
            "complaint": "Scored 55/100 on assignment but expected higher. Want re-evaluation. What's the process?"
        },
        {
            "subject": "Library Card Issue",
            "complaint": "My library card is suspended but I have no dues or overdue books. Please help."
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n{'─'*80}")
        print(f"TEST {i}: {test['subject']}")
        print(f"{'─'*80}")
        
        try:
            result = agent.handle_complaint(
                subject=test['subject'],
                complaint=test['complaint']
            )
            
            print(f"\n✓ Status: {result['status']}")
            print(f"\n📋 Resolution Preview:")
            print(f"{result['result'][:300]}...")
            
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)


def main():
    load_dotenv()
    
    print("="*80)
    print("UNIVERSITY COMPLAINT AGENT - LOCAL EMBEDDINGS + GEMINI")
    print("="*80)
    print("💾 Embeddings: LOCAL (sentence-transformers) - 100% FREE")
    print("🧠 Generation: GEMINI API - FREE TIER")
    print("💰 Total Cost: $0.00")
    print("="*80)
    
    # print("\n[1/5] Creating directories...")
    # create_directories()
    
    print("\n[2/5] Checking documents...")
    check_pdf_documents()

    
    print("\n[3/5] Checking API key...")
    API_KEY = os.getenv("GOOGLE_API_KEY")
    
    if not API_KEY:
        print("\n⚠ GOOGLE_API_KEY not found!")
        print("\n🔑 Get FREE Gemini API key:")
        print("   https://aistudio.google.com/app/apikey")
        print("\n💡 Set it in .env file:")
        print('   GOOGLE_API_KEY=your-key')
        return
    
    print(f"\n✓ API key found: {API_KEY[:8]}...{API_KEY[-4:]}")
    
    print("\n[4/5] Initializing agent...")
    print("\n⏳ First run takes 2-3 minutes:")
    print("   1. Downloading embedding model (~80MB)")
    print("   2. Building vector index locally")
    print("\n💡 Subsequent runs will be much faster!")
    
    try:
        agent = UniversityComplaintAgent(
            api_key=API_KEY,
            documents_path=DOCUMENTS_PATH,
            excel_path=EXCEL_PATH,
            chroma_path=CHROMA_PATH,
            rebuild_index=True,
            model_name=GEMINI_MODEL,
            embedding_model=EMBEDDING_MODEL
        )
        
        print("\n✓ Agent ready!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Install: pip install -r requirements.txt")
        print("   2. Check documents in data/documents/university_rules/")
        print("   3. Verify API key is valid")
        import traceback
        traceback.print_exc()
        return
    
    print("\n[5/5] Running tests...")
    run_tests(agent)
    
    print("\n" + "="*80)
    print("SETUP COMPLETE! 🎉")
    print("="*80)
    print(f"\n📊 Results in: {EXCEL_PATH}")
    print(f"💾 Vector DB in: {CHROMA_PATH}")


if __name__ == "__main__":
    main()