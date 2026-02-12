# app.py

from flask import Flask
from dotenv import load_dotenv
import os

from src.agents.university_complaint_agent import UniversityComplaintAgent
from src.api.routes import register_routes
from src.middleware.error_handler import register_error_handlers
from config.settings import (
    DOCUMENTS_PATH,
    EXCEL_PATH,
    CHROMA_PATH,
    EMBEDDING_MODEL,
    GEMINI_MODEL
)

load_dotenv()

app = Flask(__name__)

# Initialize agent once at startup
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

agent = UniversityComplaintAgent(
    api_key=API_KEY,
    documents_path=DOCUMENTS_PATH,
    excel_path=EXCEL_PATH,
    chroma_path=CHROMA_PATH,
    rebuild_index=False,
    model_name=GEMINI_MODEL,
    embedding_model=EMBEDDING_MODEL
)

# Register routes and error handlers
register_routes(app, agent)
register_error_handlers(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)