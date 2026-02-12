# scripts/add_documents.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import DOCUMENTS_PATH

def main():
    print("="*60)
    print("ADD UNIVERSITY DOCUMENTS")
    print("="*60)
    
    docs_path = Path(DOCUMENTS_PATH)
    
    print(f"\n📁 Documents directory: {docs_path}")
    print("\nSupported formats: .txt, .pdf, .docx, .md")
    print("\nInstructions:")
    print(f"1. Copy your university policy documents to: {docs_path}")
    print("2. Run: python scripts/rebuild_index.py")
    print("3. Restart the application")
    
    existing = list(docs_path.glob("*"))
    if existing:
        print(f"\n📄 Current files ({len(existing)}):")
        for f in existing:
            if f.is_file():
                print(f"  - {f.name}")

if __name__ == "__main__":
    main()