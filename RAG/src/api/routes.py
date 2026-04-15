import os
import json
import time
import signal
import sys
from datetime import datetime, timedelta
from redis import Redis
from dotenv import load_dotenv
import requests
from flask import request, jsonify


from src.agents.university_complaint_agent import UniversityComplaintAgent

load_dotenv()

# ─── Config ───────────────────────────────────────────────────────────────────
NODE_CALLBACK_URL = os.getenv("NODE_CALLBACK_URL", "http://localhost:3000/internal/ai-callback")
INTERNAL_SECRET   = os.getenv("INTERNAL_SECRET", "")
WORKER_DURATION   = int(os.getenv("WORKER_DURATION_SECONDS", 3600))  # 1 hour default
POLL_INTERVAL     = int(os.getenv("POLL_INTERVAL_SECONDS", 5))       # check every 5s when idle

# ─── Graceful shutdown flag ────────────────────────────────────────────────────
shutdown_requested = False

def handle_shutdown(signum, frame):
    global shutdown_requested
    print("\n⚠️  Shutdown signal received. Finishing current task then exiting...")
    shutdown_requested = True

signal.signal(signal.SIGINT,  handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

# ─── Redis Connection ──────────────────────────────────────────────────────────
def connect_redis():
    try:
        redis_url = os.getenv("REDIS_URL")

        if not redis_url:
            # fallback for local dev
            redis_url = "redis://127.0.0.1:6379"

        r = Redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=5
        )

        r.ping()
        print("✅ Connected to Redis")
        return r

    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        sys.exit(1)

# ─── Agent Init ───────────────────────────────────────────────────────────────
def init_agent():
    try:
        agent = UniversityComplaintAgent(
            api_key=os.getenv("GOOGLE_API_KEY"),
            documents_path="./documents",
            excel_path="./logs/complaints.xlsx",
            chroma_path="./chroma_db"
        )
        print("✅ Agent initialized")
        return agent
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        sys.exit(1)

# ─── Process a single complaint ───────────────────────────────────────────────
def process_complaint(agent, complaint_data):
    complaint_id  = complaint_data.get("_id")
    subject       = complaint_data.get("subject", "")
    complaint_text = complaint_data.get("complaintText", "")
    student_name  = complaint_data.get("studentName", "Anonymous")

    if not complaint_id:
        print("⚠️  Skipping complaint with no _id")
        return False

    print(f"🔄 Processing complaint [{complaint_id}] — {subject[:50]}")

    # Generate AI draft
    try:
        response_dict = agent.handle_complaint(
            subject=subject,
            complaint=complaint_text,
            student_name=student_name
        )
        final_text = response_dict.get("result", "").strip()
        if not final_text:
            final_text = "We have received your complaint and will look into it shortly."
    except Exception as e:
        print(f"❌ Agent error for [{complaint_id}]: {e}")
        final_text = "We have received your complaint and will look into it shortly."

    # Call Node.js internal API
    try:
        callback_res = requests.post(
            NODE_CALLBACK_URL,
            json={
                "complaintId": complaint_id,
                "aiDraft": final_text
            },
            headers={
                "Content-Type": "application/json",
                "x-internal-secret": INTERNAL_SECRET
            },
            timeout=10
        )

        if callback_res.status_code == 200:
            print(f"✅ Notified Node.js for [{complaint_id}]")
            return True
        else:
            print(f"❌ Node.js callback failed [{complaint_id}]: {callback_res.status_code} — {callback_res.text}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot reach Node.js server at {NODE_CALLBACK_URL}")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Node.js callback timed out for [{complaint_id}]")
        return False
    except Exception as e:
        print(f"❌ Callback error for [{complaint_id}]: {e}")
        return False

# ─── Main Worker Loop ─────────────────────────────────────────────────────────
def run_worker(r, agent, duration_seconds):
    start_time   = datetime.now()
    end_time     = start_time + timedelta(seconds=duration_seconds)
    processed    = 0
    failed       = 0

    print(f"\n🚀 Worker started at {start_time.strftime('%H:%M:%S')}")
    print(f"⏰ Will run until {end_time.strftime('%H:%M:%S')} ({duration_seconds}s)\n")

    while datetime.now() < end_time and not shutdown_requested:
        try:
            # rpop fetches from queue (FIFO with lPush+rpop)
            data_str = r.rpop("task_queue")

            if data_str is None:
                # Queue is empty — wait and poll again
                remaining = (end_time - datetime.now()).seconds
                print(f"💤 Queue empty. Waiting {POLL_INTERVAL}s... ({remaining}s remaining)")
                time.sleep(POLL_INTERVAL)
                continue

            complaint_data = json.loads(data_str)
            success = process_complaint(agent, complaint_data)

            if success:
                processed += 1
            else:
                failed += 1

        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in queue: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            failed += 1
            time.sleep(2)  # brief pause before retrying on unexpected errors

    # ─── Summary ──────────────────────────────────────────────────────────────
    end_reason = "shutdown signal" if shutdown_requested else "time limit reached"
    print(f"\n{'='*50}")
    print(f"🏁 Worker stopped — {end_reason}")
    print(f"   Started  : {start_time.strftime('%H:%M:%S')}")
    print(f"   Stopped  : {datetime.now().strftime('%H:%M:%S')}")
    print(f"   ✅ Processed : {processed}")
    print(f"   ❌ Failed    : {failed}")
    print(f"{'='*50}\n")

def register_routes(app, agent):

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    @app.route("/complaint", methods=["POST"])
    def create_complaint():
        try:
            data = request.json

            subject = data.get("subject", "")
            complaint = data.get("complaint", "")
            student_name = data.get("studentName", "Anonymous")

            if not subject or not complaint:
                return jsonify({"error": "subject and complaint required"}), 400

            result = agent.handle_complaint(
                subject=subject,
                complaint=complaint,
                student_name=student_name
            )

            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    r     = connect_redis()
    agent = init_agent()
    run_worker(r, agent, WORKER_DURATION)