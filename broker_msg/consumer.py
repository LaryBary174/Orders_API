from faststream import FastStream
from faststream.rabbit import RabbitBroker
import asyncio

import logging

from core.config import settings
from celery_tasks.tasks import process_order_task

logger = logging.getLogger("orders.consumer")
logging.basicConfig(level=logging.INFO)

broker = RabbitBroker(settings.BROKER_URL)

app = FastStream(broker)


@broker.subscriber("orders")
async def handle_order(msg):
    await asyncio.to_thread(process_order_task.delay, msg)
    logger.info("Forwarded order to Celery (order_id=%s)", msg.get("id"))


if __name__ == "__main__":
    asyncio.run(app.run())
