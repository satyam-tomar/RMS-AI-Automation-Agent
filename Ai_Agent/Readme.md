# University Complaint Resolution AI Agent

A production-ready AI agent that uses **LlamaIndex RAG** for knowledge retrieval and **LangChain** for intelligent agent orchestration to handle university complaints based on official rules and regulations.

## 🏗️ Architecture

### Components

1. **LlamaIndex RAG System**
   - Document loading from `./university_rules/` directory
   - Chunking and embedding generation (OpenAI embeddings)
   - Vector storage using ChromaDB
   - Query engine for semantic search

2. **LangChain Agent**
   - Two-tool setup: RAG search + Excel update
   - Conversation memory (last 2 exchanges)
   - System prompt for university compliance
   - OpenAI LLM backend

3. **Excel Logging**
   - Automatic complaint tracking in `complaints.xlsx`
   - Timestamp, subject, resolution logging

## 📋 Requirements

- Python 3.9+
- OpenAI API key
- University rules documents (.txt, .pdf, .docx, .md)

## 🚀 Installation

### 1. Clone/Download the Project

```bash
# Create project directory
mkdir complaint-agent
cd complaint-agent
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Or set it directly in the code (see Configuration section).

### 5. Prepare University Rules Documents

Create a folder structure:

```
complaint-agent/
├── university_rules/
│   ├── attendance_policy.txt
│   ├── grading_guidelines.pdf
│   ├── student_conduct.docx
│   └── academic_regulations.md
├── main.py
├── requirements.txt
├── .env
└── README.md
```

**Important**: Add your university's actual policy documents to the `university_rules/` folder. The agent's quality depends on the documents you provide.

### Example Document (attendance_policy.txt)

```text
UNIVERSITY ATTENDANCE POLICY

1. Minimum Attendance Requirement
Students must maintain at least 75% attendance in each course to be eligible for final examinations.

2. Medical Leave
Students with valid medical certificates can be granted attendance exemptions for up to 2 weeks per semester.
Medical certificates must be submitted within 3 days of return to campus.

3. Attendance Shortage Appeals
Students falling short of 75% attendance due to documented medical reasons may submit an appeal to the Academic Council.
The council will review each case individually and may grant conditional exam permission.

4. Consequences of Low Attendance
- Below 75%: Not eligible for final exams (without appeal)
- Below 65%: Automatic course withdrawal
- Below 50%: Academic probation
```

## 💻 Usage

### Basic Usage

```python
from main import UniversityComplaintAgent

# Initialize agent
agent = UniversityComplaintAgent(
    api_key="your_openai_api_key",
    documents_path="./university_rules",
    excel_path="./complaints.xlsx",
    chroma_path="./chroma_db",
    rebuild_index=False  # Set True for first run or to rebuild
)

# Handle a complaint
result = agent.handle_complaint(
    subject="Attendance Shortage",
    complaint=(
        "I have only 65% attendance due to medical reasons. "
        "I have medical certificates. Can I appear for exams?"
    )
)

print(f"Resolution: {result['result']}")
```

### Running the Example

```bash
# Make sure you're in the virtual environment
python main.py
```

### First Run

On the **first run**, set `rebuild_index=True` to build the vector database:

```python
agent = UniversityComplaintAgent(
    api_key="YOUR_API_KEY",
    rebuild_index=True  # Build index from documents
)
```

On subsequent runs, set `rebuild_index=False` to load the existing index (much faster).

## 🔧 Configuration Options

### UniversityComplaintAgent Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | Required | OpenAI API key |
| `documents_path` | str | `"./university_rules"` | Path to university documents |
| `excel_path` | str | `"./complaints.xlsx"` | Path to complaints Excel file |
| `chroma_path` | str | `"./chroma_db"` | Path to ChromaDB storage |
| `rebuild_index` | bool | `False` | Rebuild vector index from scratch |

### LlamaIndex Settings

Configured in `_setup_llamaindex()`:
- **Model**: gpt-3.5-turbo
- **Embeddings**: text-embedding-ada-002
- **Chunk Size**: 512 tokens
- **Chunk Overlap**: 50 tokens

### LangChain Agent Settings

Configured in `_setup_langchain_agent()`:
- **Memory**: Last 2 conversation turns
- **Max Iterations**: 5
- **Temperature**: 0.2 (low for consistency)

## 🛠️ How It Works

### Agent Flow

```
1. User calls handle_complaint(subject, complaint)
   ↓
2. Query constructed: "Subject: X\nComplaint: Y"
   ↓
3. LangChain agent receives query
   ↓
4. Agent uses university_rules_search tool
   ↓
5. LlamaIndex RAG searches vector database
   ↓
6. Relevant rules retrieved and analyzed
   ↓
7. Agent formulates response based on rules
   ↓
8. Agent calls update_excel_sheet tool
   ↓
9. Complaint logged to complaints.xlsx
   ↓
10. Final response returned to user
```

### Tools Available to Agent

1. **university_rules_search**
   - Searches the knowledge base
   - Returns relevant policy excerpts
   - Used for every complaint resolution

2. **update_excel_sheet**
   - Records complaint details
   - Logs resolution and timestamp
   - Creates audit trail

## 📊 Output Format

### Function Return Value

```python
{
    "subject": "Attendance Shortage",
    "complaint": "I have only 65% attendance...",
    "result": "Based on university policy...",
    "status": "success"  # or "error"
}
```

### Excel Output

The `complaints.xlsx` file contains:

| Timestamp | Student Name | Subject | Complaint | Resolution | Status |
|-----------|--------------|---------|-----------|------------|--------|
| 2025-12-09 14:30:25 | Anonymous | Attendance Shortage | I have only 65%... | Based on policy... | Resolved |

## 🔍 Troubleshooting

### Issue: "No documents found"

**Solution**: Add .txt, .pdf, .docx, or .md files to the `./university_rules/` folder.

### Issue: OpenAI API errors

**Solution**: 
- Check your API key is valid
- Ensure you have API credits
- Check rate limits

### Issue: ChromaDB errors

**Solution**: Delete the `./chroma_db/` folder and rebuild with `rebuild_index=True`

### Issue: Agent not finding rules

**Solution**: 
- Rebuild index: `rebuild_index=True`
- Check document quality and formatting
- Increase `similarity_top_k` in query engine

## 🎯 Best Practices

1. **Document Quality**: Provide clear, well-structured policy documents
2. **Index Management**: Rebuild index when documents are updated
3. **API Costs**: Use gpt-3.5-turbo for cost efficiency
4. **Monitoring**: Check `complaints.xlsx` regularly for audit trail
5. **Testing**: Test with various complaint types before production

## 🔐 Security Notes

- Never commit your `.env` file or API keys
- Add `.env` and `chroma_db/` to `.gitignore`
- Sanitize student data in production
- Implement authentication before deploying

## 📝 Customization

### Modify System Prompt

Edit the `system_message` in `_setup_langchain_agent()`:

```python
system_message = """Your custom prompt here..."""
```

### Add More Tools

Add new tools to the `tools` list:

```python
tools.append(
    Tool(
        name="your_tool_name",
        func=your_function,
        description="Tool description"
    )
)
```

### Change LLM Provider

Replace OpenAI with other providers:

```python
from langchain.llms import Anthropic  # or other provider

self.llm = Anthropic(api_key="YOUR_KEY")
```

## 📦 Project Structure

```
complaint-agent/
├── main.py                 # Main agent code
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .env                   # Environment variables (create this)
├── university_rules/      # Policy documents (create this)
│   └── *.txt, *.pdf, etc.
├── chroma_db/            # Vector database (auto-created)
└── complaints.xlsx       # Complaint log (auto-created)
```

## 🚀 Production Deployment

For production use:

1. Add proper authentication
2. Implement rate limiting
3. Add input validation
4. Set up monitoring and logging
5. Use environment variables for all configs
6. Deploy with HTTPS
7. Regular backup of `complaints.xlsx`
8. Implement role-based access control

## 📄 License

This is a template project for educational purposes.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review LlamaIndex docs: https://docs.llamaindex.ai
3. Review LangChain docs: https://docs.langchain.com

## 🎓 Example Scenarios

### Scenario 1: Attendance Appeal
```python
result = agent.handle_complaint(
    subject="Attendance Below 75%",
    complaint="Medical emergency, have certificates"
)
```

### Scenario 2: Grade Dispute
```python
result = agent.handle_complaint(
    subject="Unfair Grading",
    complaint="Assignment graded incorrectly, request review"
)
```

### Scenario 3: Facility Issue
```python
result = agent.handle_complaint(
    subject="Library Access Problem",
    complaint="Card not working, no pending dues"
)
```

---

**Ready to deploy?** Follow the installation steps and customize for your university's needs!