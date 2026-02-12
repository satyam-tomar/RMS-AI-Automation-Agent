# src/rag/query_engine.py

from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_query_engine(index, similarity_top_k: int):
    logger.info(f"Creating query engine with top_k={similarity_top_k}")
    
    query_engine = index.as_query_engine(
        similarity_top_k=similarity_top_k,
        response_mode="compact"
    )
    
    return query_engine