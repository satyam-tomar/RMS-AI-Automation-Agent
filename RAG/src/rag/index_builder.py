# src/rag/index_builder.py

from pathlib import Path
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.rag.document_loader import load_documents
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_rag_index(documents_path: Path, chroma_path: Path):
    logger.info("Building RAG index with LOCAL embeddings...")
    logger.info("(This happens on your Mac - no API calls!)")
    
    documents = load_documents(documents_path)
    
    chroma_client = chromadb.PersistentClient(path=str(chroma_path))
    chroma_collection = chroma_client.get_or_create_collection("university_rules")
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    
    logger.info("✓ Index built with local embeddings!")
    return index


def load_rag_index(chroma_path: Path):
    chroma_client = chromadb.PersistentClient(path=str(chroma_path))
    chroma_collection = chroma_client.get_or_create_collection("university_rules")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    index = VectorStoreIndex.from_vector_store(vector_store)
    logger.info("✓ Existing index loaded")
    return index