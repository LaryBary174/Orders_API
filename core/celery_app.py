from celery import Celery
from .config import settings

celery_app = Celery(
    "order_tasks",
    backend="rpc://",
    broker=settings.BROKER_URL,
    include=["celery_tasks.tasks"],
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
