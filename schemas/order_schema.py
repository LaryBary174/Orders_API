from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from database.models import OrderStatus


class OrderItem(BaseModel):
    name: str


class OrderCreate(BaseModel):
    items: Optional[List[OrderItem]] | None = None
    total_price: Decimal
    status: Optional[OrderStatus] = OrderStatus.PENDING

    class Config:
        from_attributes = True


class OrderRead(BaseModel):
    id: UUID
    user_id: int
    items: Optional[List[OrderItem]] = None
    total_price: Decimal
    status: OrderStatus
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

    class Config:
        from_attributes = True