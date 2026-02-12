import os

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Paths
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", "./data/documents/university_rules")
EXCEL_PATH = os.getenv("EXCEL_PATH", "./data/complaints.xlsx")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/vector_store/chroma_db")

# LlamaIndex Settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
SIMILARITY_TOP_K = int(os.getenv("SIMILARITY_TOP_K", "3"))
EMBED_BATCH_SIZE = 32
MAX_SEQ_LENGTH = 256

# Gemini Settings
TEMPERATURE = 0.1