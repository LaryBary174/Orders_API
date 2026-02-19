from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from broker_msg.producer import publish_order
from core.dependencies import get_current_user
from core.redis import get_redis
from database.db import db_engine
from schemas.order_schema import OrderUpdate, OrderCreate, OrderRead
from services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


def get_order_service(
        session: AsyncSession = Depends(db_engine.session_dependency),
        redis_client: Redis = Depends(get_redis)
) -> OrderService:
    return OrderService(session, redis_client)



@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
        order_data: OrderCreate,
        current_user = Depends(get_current_user),
        service: OrderService = Depends(get_order_service)
):
    order = await service.create_order(current_user.id, order_data)
    order_dict = OrderRead.model_validate(order).model_dump()
    await publish_order(order_dict, routing_key="orders")
    return OrderRead.model_validate(order)


@router.get("/user/{user_id}/", response_model=list[OrderRead])
async def get_user_orders(
        user_id: int,
        limit: int = 50,
        offset: int = 0,
        current_user = Depends(get_current_user),
        service: OrderService = Depends(get_order_service)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    orders = await service.get_orders_by_user_id(user_id, limit, offset)
    return [OrderRead.model_validate(order) for order in orders]


@router.get("/{order_id}/", response_model=OrderRead)
async def get_order(
        order_id: UUID,
        service: OrderService = Depends(get_order_service)
):
    order = await service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if isinstance(order, dict):
        return OrderRead(**order)

    return OrderRead.model_validate(order)


@router.patch("/{order_id}/", response_model=OrderRead)
async def update_order(
        order_id: UUID,
        order_in: OrderUpdate,
        service: OrderService = Depends(get_order_service)
):
    order = await service.update_order_status(order_id, order_in.status)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return OrderRead.model_validate(order)