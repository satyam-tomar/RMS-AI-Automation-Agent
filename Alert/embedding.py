from sentence_transformers import SentenceTransformer
import numpy as np

# Load a small, efficient embedding model
_model = None

def _get_model():
    """
    Lazy-load the embedding model to avoid loading at import time.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def embed_text(text):
    """
    Converts text into a dense embedding vector.
    
    Args:
        text (str): Input complaint text
        
    Returns:
        np.ndarray: Embedding vector
    """
    model = _get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.reshape(1, -1)