# scripts/rebuild_index.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
from dotenv import load_dotenv
from src.agents.university_complaint_agent import UniversityComplaintAgent
from config.settings import DOCUMENTS_PATH, EXCEL_PATH, CHROMA_PATH, EMBEDDING_MODEL, GEMINI_MODEL

load_dotenv()

def main():
    print("="*60)
    print("REBUILDING VECTOR INDEX")
    print("="*60)
    
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        print("❌ GOOGLE_API_KEY not found in .env")
        return
    
    print("\n⏳ This will rebuild the entire vector index...")
    print("📁 Loading documents from:", DOCUMENTS_PATH)
    
    agent = UniversityComplaintAgent(
        api_key=API_KEY,
        documents_path=DOCUMENTS_PATH,
        excel_path=EXCEL_PATH,
        chroma_path=CHROMA_PATH,
        rebuild_index=True,
        model_name=GEMINI_MODEL,
        embedding_model=EMBEDDING_MODEL
    )
    
    print("\n✅ Index rebuilt successfully!")
    print(f"💾 Saved to: {CHROMA_PATH}")

if __name__ == "__main__":
    main()