# src/llms/gemini_client.py

import google.generativeai as genai

from src.utils.logger import get_logger

logger = get_logger(__name__)


def initialize_gemini(api_key: str, model_name: str):
    logger.info(f"Initializing Gemini: {model_name}")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    logger.info("✓ Gemini initialized")
    return model