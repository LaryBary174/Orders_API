import asyncio
import logging
from faststream.rabbit.fastapi import RabbitRouter
from core.config import settings

logger = logging.getLogger("orders.producer")
router = RabbitRouter(settings.BROKER_URL)


async def start_broker():
    await asyncio.sleep(20)
    await router.broker.connect()
    logger.info("Rabbit broker connected")


async def stop_broker():
    await router.broker.stop()
    logger.info("Rabbit broker disconnected")


async def publish_order(payload: dict, routing_key: str = "orders"):
    await router.broker.publish(payload, routing_key)
    logger.info(f"Order published to '{routing_key}'")
