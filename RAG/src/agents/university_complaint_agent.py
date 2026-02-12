from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import os

import google.generativeai as genai
from llama_index.llms.gemini import Gemini as LlamaGemini
from llama_index.core import Settings

from src.rag.index_builder import build_rag_index, load_rag_index
from src.rag.query_engine import create_query_engine
from src.llms.gemini_client import initialize_gemini
from src.storage.excel_logger import ExcelLogger
from src.embeddings.local_embedding import LocalEmbedding
from src.utils.logger import get_logger
from config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TEMPERATURE,
    SIMILARITY_TOP_K
)

logger = get_logger(__name__)

class UniversityComplaintAgent:
    
    def __init__(
        self,
        api_key: str,
        documents_path: str,
        excel_path: str,
        chroma_path: str,
        rebuild_index: bool = False,
        model_name: str = "gemini-2.5-flash",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        self.api_key = api_key
        self.documents_path = Path(documents_path)
        self.excel_path = Path(excel_path)
        self.chroma_path = Path(chroma_path)
        self.model_name = model_name
        self.embedding_model = embedding_model
        
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=api_key)
        
        self.llm = genai.GenerativeModel(model_name)
        
        self._setup_llamaindex()
        self.excel_logger = ExcelLogger(self.excel_path)
        self._setup_rag_index(rebuild_index)
        
        logger.info("="*60)
        logger.info("AGENT READY!")
        logger.info("="*60)
        logger.info(f"💾 Embeddings: {embedding_model}")
        logger.info(f"🧠 Generation: {model_name}")
        logger.info("="*60)
    
    def _setup_llamaindex(self) -> None:
        Settings.embed_model = LocalEmbedding(model_name=self.embedding_model)
        Settings.llm = LlamaGemini(
            model_name=f"models/{self.model_name}",
            api_key=self.api_key,
            temperature=TEMPERATURE
        )
        Settings.chunk_size = CHUNK_SIZE
        Settings.chunk_overlap = CHUNK_OVERLAP
        
        logger.info("✓ LlamaIndex configured with local embeddings")
    
    def _setup_rag_index(self, rebuild: bool) -> None:
        if rebuild or not self.chroma_path.exists():
            logger.info("Building RAG index with LOCAL embeddings...")
            self.index = build_rag_index(self.documents_path, self.chroma_path)
        else:
            logger.info("Loading existing index...")
            self.index = load_rag_index(self.chroma_path)
        
        self.query_engine = create_query_engine(self.index, SIMILARITY_TOP_K)
    
    def _search_rules(self, query: str) -> str:
        try:
            response = self.query_engine.query(query)
            return str(response)
        except Exception as e:
            logger.error(f"Search error: {e}")
            return f"Error searching rules: {str(e)}"
    
    def handle_complaint(
        self,
        subject: str,
        complaint: str,
        student_name: str = "Anonymous"
    ) -> Dict[str, Any]:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {subject}")
        logger.info(f"{'='*60}")
        
        try:
            logger.info("🔍 Searching policies with LOCAL embeddings...")
            search_query = f"Find university policies about: {subject}. Full complaint: {complaint}"
            rules_context = self._search_rules(search_query)
            logger.info("✓ Policy search complete (no API cost!)")
            
            logger.info("🧠 Generating resolution with Gemini...")
            prompt = f"""
You are acting as a university teacher reviewing a student complaint.

REFERENCE INFORMATION:
{rules_context}

COMPLAINT DETAILS:
Subject: {subject}
Description: {complaint}

RESPONSE GUIDELINES:
- Write a factual resolution after reviewing the complaint and reference information.
- Keep the response strictly between 4 and 7 lines.
- Do NOT include greetings, names, or polite phrases (e.g., “thank you for reaching out”).
- Do NOT repeatedly mention policies or highlight them unnecessarily.
- Clearly state what was reviewed, identify the cause or finding, and give the final conclusion.
- Use a neutral, authoritative tone, as a teacher explaining verified findings.
- No emotional language, no escalation suggestions unless absolutely required.
- No closing remarks or formal sign-offs.

Generate only the final response text.
"""

            response = self.llm.generate_content(prompt)
            resolution = response.text
            logger.info("✓ Resolution generated")
            
            logger.info("💾 Logging to Excel...")
            self.excel_logger.log_complaint(student_name, subject, complaint, resolution)
            
            result = {
                "student_name": student_name,
                "subject": subject,
                "complaint": complaint,
                "result": resolution,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Complaint resolved successfully!")
            return result
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(error_msg)
            
            return {
                "student_name": student_name,
                "subject": subject,
                "complaint": complaint,
                "result": f"System error. Please contact support. Error: {str(e)}",
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }