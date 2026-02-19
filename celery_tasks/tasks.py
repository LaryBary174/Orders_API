import asyncio
import logging
from typing import Dict, Any

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from core.celery_app import celery_app
from core.config import settings
from database.models import OrderStatus
from services.order_service import OrderService

logger = logging.getLogger("orders.tasks")


async def process_order(order: Dict[str, Any]) -> Dict[str, Any]:
    order_id = order["id"]
    logger.info(f"start processing order {order_id}")

    await asyncio.sleep(10)

    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    try:
        async with session_factory() as session:
            service = OrderService(session=session, redis_client=None)
            update = await service.update_order_status(
                order_id=order_id, status=OrderStatus.SHIPPED
            )
            status_value = None
            if update is not None:
                status_value = (
                    str(update.status.value)
                    if hasattr(update.status, "value")
                    else str(update.status)
                )
    finally:
        await engine.dispose()

    logger.info(f"Order {order_id} processed")
    return {"order_id": str(order_id), "status": status_value}


@celery_app.task(bind=True, name="process_order", acks_late=True)
def process_order_task(self, order: Dict[str, Any]):
    result = asyncio.run(process_order(order))
    return result
