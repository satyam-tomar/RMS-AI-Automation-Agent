# app.py
from flask import Flask
from dotenv import load_dotenv
import os
import threading

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

from src.api.routes import connect_redis, run_worker

load_dotenv()

app = Flask(__name__)

# ─── Init Agent ───────────────────────────────────────────────────────────────
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

agent = UniversityComplaintAgent(
    api_key=API_KEY,
    documents_path=DOCUMENTS_PATH,
    excel_path=EXCEL_PATH,
    chroma_path=CHROMA_PATH,
    rebuild_index=True,
    model_name=GEMINI_MODEL,
    embedding_model=EMBEDDING_MODEL
)

# ─── Register Flask routes & error handlers ───────────────────────────────────
register_routes(app, agent)
register_error_handlers(app)

# ─── Start Redis worker in background thread ──────────────────────────────────
def start_worker():
    r = connect_redis()
    duration = int(os.getenv("WORKER_DURATION_SECONDS", 3600))
    run_worker(r, agent, duration)

worker_thread = threading.Thread(target=start_worker, daemon=True)
worker_thread.start()
print("✅ Background worker started")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)