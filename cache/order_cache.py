import json
from typing import Optional
from uuid import UUID

from redis.asyncio import Redis


class OrderCache:
    def __init__(self, redis_client: Redis, ttl: int = 300):
        self.redis_client = redis_client
        self.ttl = ttl


    async def get_order(self, order_id: UUID) -> Optional[dict]:
        key = f"order:{order_id}"
        order_data = await self.redis_client.get(key)
        if order_data:
            return json.loads(order_data)
        return None

    async def set_order(self, order_id: UUID, order_data: str):
        key = f"order:{order_id}"
        await self.redis_client.set(key, order_data, ex=self.ttl)

    async def delete_order(self, order_id: UUID):
        key = f"order:{order_id}"
        await self.redis_client.delete(key)