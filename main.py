import redis.asyncio as aioredis
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import settings
from core.middleware import configure_middlewares

from api.users import router as users_router
from api.orders import router as orders_router
from broker_msg import producer as order_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis_client = aioredis.from_url(
        settings.REDIS_URL, encoding="utf-8", decode_responses=True
    )
    await order_producer.start_broker()
    yield
    await order_producer.stop_broker()
    await app.state.redis_client.aclose()


app = FastAPI(lifespan=lifespan)
configure_middlewares(app)
app.include_router(users_router)
app.include_router(orders_router)
