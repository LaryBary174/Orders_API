from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Users


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, user_email: str) -> Optional[Users]:
        query = select(Users).where(Users.email == user_email)
        result = await self.session.execute(query)
        return result.scalars().first()


    async def create(self, user_email: str, hashed_password: str) -> Users:
        user = Users(email=user_email, password=hashed_password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
