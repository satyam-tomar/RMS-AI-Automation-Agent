import os
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

r = Redis(
    host=os.getenv("REDIS_HOST", "127.0.0.1"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD") or None,
    decode_responses=True
)

# Check if Redis is alive
try:
    r.ping()
    print("✅ Connected to Redis")
except Exception as e:
    print("❌ Redis connection failed:", e)
    exit(1)

# Count items in task queue
queue_length = r.llen("task_queue")
print(f"📦 Items in 'task_queue': {queue_length}")

# Optional: list all keys in Redis
all_keys = r.keys("*")
print(f"\n🔑 Total keys in Redis: {len(all_keys)}")
print("Keys:", all_keys)