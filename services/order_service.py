import json
from decimal import Decimal
from typing import Optional
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.order_schema import OrderCreate, OrderRead
from cache.order_cache import OrderCache
from database.models import Orders, OrderStatus
from repositories.order_repository import OrderRepository


class OrderService:

    def __init__(self, session: AsyncSession, redis_client: Optional[Redis] = None):
        self.repository = OrderRepository(session)
        self.cache = OrderCache(redis_client) if redis_client else None

    async def create_order(self, user_id: int, order_data: OrderCreate) -> Orders:
        items_json = (
            [item.model_dump() for item in order_data.items] if order_data.items else []
        )
        order = await self.repository.create(
            user_id=user_id,
            items=items_json,
            total_price=Decimal(order_data.total_price),
            status=order_data.status
        )
        return order

    async def get_order_by_id(self, order_id: UUID):
        if self.cache:
            cached_order = await self.cache.get_order(order_id)
            if cached_order:
                return cached_order
        order = await self.repository.get_order_by_id(order_id)
        if not order:
            return None

        order_dict = OrderRead.model_validate(order).model_dump_json()
        if self.cache:
            await self.cache.set_order(order_id, order_dict)
        return json.loads(order_dict)

    async def get_orders_by_user_id(
            self,
            user_id: int,
            limit: int = 50,
            offset: int = 0
        ) -> list[Orders]:
        return await self.repository.get_order_by_user_id(user_id, limit, offset)


    async def update_order_status(self, order_id: UUID, status: OrderStatus) -> Optional[Orders]:
        order = await self.repository.update_status(order_id, status)
        if not order:
            return None
        if self.cache:
            order_dict = OrderRead.model_validate(order).model_dump_json()
            await self.cache.set_order(order_id, order_dict)
        return order
