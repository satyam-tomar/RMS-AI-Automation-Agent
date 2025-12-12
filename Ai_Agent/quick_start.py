"""
Quick Start - Local Embeddings + Gemini Brain (100% FREE!)
"""

import os
import sys
from pathlib import Path


def create_directories():
    """Create necessary directories"""
    for directory in ["./university_rules", "./chroma_db"]:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created: {directory}")


def create_sample_rules():
    """Create sample university rules document"""
    rules_dir = Path("./university_rules")
    existing = list(rules_dir.glob("*.txt"))
    
    if not existing:
        print("\n⚠ No documents found, creating sample...")
        
        sample = """UNIVERSITY ATTENDANCE POLICY

1. MINIMUM ATTENDANCE REQUIREMENT
- Students must maintain at least 75% attendance
- Required for final exam eligibility

2. MEDICAL LEAVE PROVISIONS
- Valid medical certificates: up to 2 weeks excused
- From registered practitioners only
- Submit within 3 days of return
- Medical days excluded from calculation

3. ATTENDANCE APPEALS
Students below 75% may appeal if:
- Documented medical/emergency reasons
- Good academic standing (CGPA > 6.0)
- Submit within 5 days of notification

Appeal Process:
- Written appeal to Department Head
- Include supporting documentation
- Review within 5 working days
- May grant conditional exam permission

4. CONSEQUENCES
- 70-74%: Warning
- 65-69%: Mandatory counseling
- Below 65%: Not eligible without appeal
- Below 50%: Automatic withdrawal

5. GRADE RE-EVALUATION
- Request within 5 days of publication
- Fee: ₹500 (refunded if grade changes)
- Different faculty reviews
- Decision is final

6. LIBRARY ISSUES
Card suspended if:
- Overdue books (>30 days)
- Unpaid fines (>₹1000)
- Damaged property

Resolution:
- Check dues at counter
- Verify student status
- Contact library@university.edu
- Resolved within 24 hours
"""
        
        (rules_dir / "university_policies.txt").write_text(sample)
        print("✓ Created sample policy document")
        print("📄 Replace with your actual policies!")
    else:
        print(f"✓ Found {len(existing)} documents")


def check_api_key():
    """Check Gemini API key"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("\n⚠ GOOGLE_API_KEY not found!")
        print("\n🔑 Get FREE Gemini API key:")
        print("   https://aistudio.google.com/app/apikey")
        print("\n💡 Set it:")
        print('   export GOOGLE_API_KEY="your-key"')
        print("   OR create .env file with:")
        print('   GOOGLE_API_KEY=your-key')
        return None
    
    masked = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
    print(f"\n✓ API key found: {masked}")
    return api_key


def run_tests(agent):
    """Run test complaints"""
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
    """Main setup function"""
    print("="*80)
    print("UNIVERSITY COMPLAINT AGENT - LOCAL EMBEDDINGS + GEMINI")
    print("="*80)
    print("💾 Embeddings: LOCAL (sentence-transformers) - 100% FREE")
    print("🧠 Generation: GEMINI API - FREE TIER")
    print("💰 Total Cost: $0.00")
    print("="*80)
    
    print("\n[1/5] Creating directories...")
    create_directories()
    
    print("\n[2/5] Checking documents...")
    create_sample_rules()
    
    print("\n[3/5] Checking API key...")
    api_key = check_api_key()
    
    if not api_key:
        print("\n❌ Cannot proceed without API key")
        print("Get it here: https://aistudio.google.com/app/apikey")
        return
    
    print("\n[4/5] Initializing agent...")
    print("\n⏳ First run takes 2-3 minutes:")
    print("   1. Downloading embedding model (~80MB)")
    print("   2. Building vector index locally")
    print("\n💡 Subsequent runs will be much faster!")
    
    try:
        from main import UniversityComplaintAgent
        
        agent = UniversityComplaintAgent(
            api_key=api_key,
            rebuild_index=True,
            embedding_model="all-MiniLM-L6-v2"  # 80MB, perfect for M1
        )
        
        print("\n✓ Agent ready!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Install: pip install -r requirements.txt")
        print("   2. Check documents in ./university_rules/")
        print("   3. Verify API key is valid")
        print("\n💡 Common issues:")
        print("   - Missing sentence-transformers: pip install sentence-transformers")
        print("   - Out of memory: Close other apps, try again")
        return
    
    print("\n[5/5] Running tests...")
    run_tests(agent)
    
    print("\n" + "="*80)
    print("SETUP COMPLETE! 🎉")
    print("="*80)
    print("\n✅ Your agent is ready!")
    print(f"\n📊 Results in: ./complaints.xlsx")
    print(f"💾 Vector DB in: ./chroma_db/")
    print(f"🤖 Embedding model cached in: ~/.cache/huggingface/")
    
    print("\n💰 COST BREAKDOWN:")
    print("   ✓ Local embeddings: $0.00 (runs on your Mac)")
    print("   ✓ Gemini generation: $0.00 (free tier: 1,500/day)")
    print("   ✓ Total: $0.00")
    
    print("\n📈 MEMORY USAGE (M1 Mac):")
    print("   - Embedding model: ~150MB RAM")
    print("   - ChromaDB: ~100-300MB")
    print("   - Agent overhead: ~200MB")
    print("   - Total: ~500-700MB (fits easily in 3-4GB free)")
    
    print("\n💻 Quick Usage:")
    print('   from main import UniversityComplaintAgent')
    print('   agent = UniversityComplaintAgent(api_key="your-key")')
    print('   result = agent.handle_complaint(')
    print('       subject="Subject",')
    print('       complaint="Complaint text"')
    print('   )')
    
    print("\n🎯 Benefits:")
    print("   ✓ Works offline for embeddings (no internet needed)")
    print("   ✓ Privacy: Your docs stay on your Mac")
    print("   ✓ Fast: Local embeddings, cached after first run")
    print("   ✓ FREE: No costs for embeddings or API calls")


if __name__ == "__main__":
    # Load .env if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    main()