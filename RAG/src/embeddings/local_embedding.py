from typing import List, Any
from sentence_transformers import SentenceTransformer
from llama_index.core.embeddings import BaseEmbedding

from src.utils.logger import get_logger
from config.settings import EMBED_BATCH_SIZE, MAX_SEQ_LENGTH

logger = get_logger(__name__)


class LocalEmbedding(BaseEmbedding):
    
    model_name: str
    _model: Any = None
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", **kwargs):
        super().__init__(
            model_name=model_name,
            embed_batch_size=EMBED_BATCH_SIZE,
            **kwargs
        )
        
        logger.info(f"Loading local embedding model: {model_name}")
        object.__setattr__(self, '_model', SentenceTransformer(model_name))
        self._model.max_seq_length = MAX_SEQ_LENGTH
        
        logger.info(f"✓ Model loaded: {model_name}")
        logger.info(f"  Embedding dimension: {self._model.get_sentence_embedding_dimension()}")
        logger.info(f"  Max sequence length: {self._model.max_seq_length}")
    
    class Config:
        arbitrary_types_allowed = True
    
    def _get_query_embedding(self, query: str) -> List[float]:
        embedding = self._model.encode(query, normalize_embeddings=True)
        return embedding.tolist()
    
    def _get_text_embedding(self, text: str) -> List[float]:
        embedding = self._model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
    
    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
            batch_size=self.embed_batch_size
        )
        return [emb.tolist() for emb in embeddings]
    
    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)
    
    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)