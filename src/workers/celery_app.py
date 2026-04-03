from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Use Redis as the broker and result backend
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "agie_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.workers.tasks"]
)

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

if __name__ == "__main__":
    celery_app.start()
