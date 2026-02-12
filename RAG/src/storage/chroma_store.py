# src/storage/chroma_store.py

import chromadb
from pathlib import Path
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.utils.logger import get_logger

logger = get_logger(__name__)


def get_chroma_store(chroma_path: Path, collection_name: str = "university_rules"):
    logger.info(f"Connecting to ChromaDB at: {chroma_path}")
    
    chroma_client = chromadb.PersistentClient(path=str(chroma_path))
    chroma_collection = chroma_client.get_or_create_collection(collection_name)
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    logger.info(f"✓ Connected to collection: {collection_name}")
    
    return vector_store, chroma_client