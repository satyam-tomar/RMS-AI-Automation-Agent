# src/rag/document_loader.py

from pathlib import Path
from llama_index.core import SimpleDirectoryReader

from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_documents(documents_path: Path):
    logger.info(f"Loading documents from: {documents_path}")
    
    documents = SimpleDirectoryReader(
        str(documents_path),
        recursive=True,
        required_exts=[".txt", ".pdf", ".docx", ".md"]
    ).load_data()
    
    logger.info(f"Loaded {len(documents)} documents")
    return documents