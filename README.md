
## University Complaint Resolution AI Agent

RAG-based complaint resolution system using local embeddings (sentence-transformers) and Gemini API for generation. Processes student complaints by searching university policies and generating resolutions.

### Setup

1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your `GOOGLE_API_KEY`
4. Add university policy documents to `data/documents/university_rules/`
5. Run setup: `python src/main.py` (first time only, builds index)

# Project Structure
```
project_root/
├── app.py                              # Flask application entry point
├── .env                                # Environment variables (API keys, secrets)
├── .gitignore                          # Git ignore rules
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Docker container build instructions
├── docker-compose.yml                  # Docker orchestration configuration
├── Makefile                            # Development command shortcuts
├── README.md                           # Project documentation
│
├── config/
│   ├── __init__.py                     # Package marker
│   └── settings.py                     # Centralized configuration settings
│
├── src/
│   ├── __init__.py                     # Package marker
│   │
│   ├── api/
│   │   ├── __init__.py                 # Package marker
│   │   └── routes.py                   # Flask API endpoints
│   │
│   ├── agents/
│   │   ├── __init__.py                 # Package marker
│   │   └── university_complaint_agent.py  # Main AI agent orchestrator
│   │
│   ├── embeddings/
│   │   ├── __init__.py                 # Package marker
│   │   └── local_embedding.py          # Local embedding model wrapper
│   │
│   ├── rag/
│   │   ├── __init__.py                 # Package marker
│   │   ├── document_loader.py          # Document loading logic
│   │   ├── index_builder.py            # Vector index creation/loading
│   │   └── query_engine.py             # RAG search engine
│   │
│   ├── llms/
│   │   ├── __init__.py                 # Package marker
│   │   └── gemini_client.py            # Gemini API client initialization
│   │
│   ├── storage/
│   │   ├── __init__.py                 # Package marker
│   │   ├── chroma_store.py             # ChromaDB vector store manager
│   │   └── excel_logger.py             # Excel logging functionality
│   │
│   ├── middleware/
│   │   ├── __init__.py                 # Package marker
│   │   └── error_handler.py            # Flask error handling middleware
│   │
│   ├── utils/
│   │   ├── __init__.py                 # Package marker
│   │   └── logger.py                   # Logging configuration
│   │
│   └── main.py                         # Standalone setup & testing script
│
├── data/
│   ├── documents/
│   │   └── university_rules/
│   │       ├── .gitkeep                # Git folder placeholder
│   │       └── sample.txt              # Sample policy document
│   │
│   ├── vector_store/
│   │   └── chroma_db/
│   │       └── .gitkeep                # Git folder placeholder
│   │
│   └── complaints.xlsx                 # Excel complaint logs (auto-generated)
│
├── logs/
│   └── .gitkeep                        # Git folder placeholder
│
├── tests/
│   ├── __init__.py                     # Package marker
│   └── test_agent.py                   # Agent unit tests
│
└── scripts/
    ├── rebuild_index.py                # Rebuild vector index script
    └── add_documents.py                # Document addition helper script
```

## File Responsibilities

### **Root Files**
| File | Purpose |
|------|---------|
| `app.py` | Flask application entry point - initializes agent and starts web server |
| `.env` | Stores secret keys and configuration (never commit to git) |
| `.gitignore` | Specifies files/folders git should ignore |
| `requirements.txt` | Lists all Python dependencies for pip install |
| `Dockerfile` | Instructions to build Docker container image |
| `docker-compose.yml` | Orchestrates Docker container deployment |
| `Makefile` | Shortcut commands for common tasks (install, run, test) |
| `README.md` | Project documentation and setup instructions |

### **config/**
Centralizes all configuration settings.

| File | Purpose |
|------|---------|
| `settings.py` | Single source of truth for all config values (model names, paths, API settings) |

### **src/api/**
Handles HTTP requests and responses.

| File | Purpose |
|------|---------|
| `routes.py` | Defines Flask endpoints (`/generate-draft`, `/health`) |

### **src/agents/**
Core AI agent logic.

| File | Purpose |
|------|---------|
| `university_complaint_agent.py` | Main agent orchestrating RAG search + Gemini generation + Excel logging |

### **src/embeddings/**
Text-to-vector conversion (runs locally).

| File | Purpose |
|------|---------|
| `local_embedding.py` | Wraps sentence-transformers model for LlamaIndex integration |

### **src/rag/**
Retrieval-Augmented Generation components.

| File | Purpose |
|------|---------|
| `document_loader.py` | Loads university policy documents from disk |
| `index_builder.py` | Builds and loads vector database index |
| `query_engine.py` | Searches vector database for relevant policies |

### **src/llms/**
Large Language Model integration.

| File | Purpose |
|------|---------|
| `gemini_client.py` | Initializes Google Gemini API client |

### **src/storage/**
Data persistence layer.

| File | Purpose |
|------|---------|
| `chroma_store.py` | Manages ChromaDB vector database connections |
| `excel_logger.py` | Logs complaints/resolutions to Excel file |

### **src/middleware/**
Flask middleware for cross-cutting concerns.

| File | Purpose |
|------|---------|
| `error_handler.py` | Catches and formats error responses |

### **src/utils/**
Helper utilities.

| File | Purpose |
|------|---------|
| `logger.py` | Configures logging for debugging and monitoring |

### **src/**
| File | Purpose |
|------|---------|
| `main.py` | Standalone setup script for first-time initialization and testing |

### **data/documents/university_rules/**
Stores university policy documents.

| File | Purpose |
|------|---------|
| `sample.txt` | Example policy document (replace with real policies) |

### **tests/**
Unit and integration tests.

| File | Purpose |
|------|---------|
| `test_agent.py` | Tests agent initialization and complaint handling |

### **scripts/**
Utility scripts for maintenance.

| File | Purpose |
|------|---------|
| `rebuild_index.py` | Rebuilds vector index when you add new documents |
| `add_documents.py` | Helper to guide adding new policy documents |

## Required `__init__.py` Files

These 10 empty files make folders importable as Python packages:
```
config/__init__.py
src/__init__.py
src/api/__init__.py
src/agents/__init__.py
src/embeddings/__init__.py
src/rag/__init__.py
src/llms/__init__.py
src/storage/__init__.py
src/utils/__init__.py
src/middleware/__init__.py
tests/__init__.py
```

## Data Flow
```
User Request → Flask (routes.py)
              ↓
       Agent (university_complaint_agent.py)
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
RAG Search          Gemini API
(local embeddings)  (generation)
    ↓                   ↓
Query Engine ──────→ Resolution
    ↓
Excel Logger
    ↓
Response to User
```

API available at `http://localhost:5000/generate-draft`