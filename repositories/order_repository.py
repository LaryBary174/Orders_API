from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import OrderStatus
from database.models import Orders


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            user_id: int,
            items: list,
            total_price: Decimal,
            status: OrderStatus = OrderStatus.PENDING
    ) -> Optional[Orders]:
        order = Orders(
            user_id=user_id,
            items=items,
            total_price=total_price,
            status=status,
        )
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_order_by_id(self, order_id: UUID) -> Optional[Orders]:
        query = select(Orders).where(Orders.id == order_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_order_by_user_id(
            self,
            user_id: int,
            limit: int = 50,
            offset: int = 0,
    ) -> List[Orders]:
        query = (
            select(Orders)
            .where(Orders.user_id == user_id)
            .order_by(Orders.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())


    async def update_status(
            self,
            order_id: UUID,
            status: OrderStatus
    ) -> Optional[Orders]:
        order = await self.get_order_by_id(order_id)
        if not order:
            return None
        order.status = status
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order