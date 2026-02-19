from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from utils.password import hash_password,verify_password
from schemas.user_schema import UserCreate
from database.models import Users
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)


    async def register(self, user_data: UserCreate) -> Optional[Users]:
        existing = await self.repository.get_by_email(user_data.email)
        if existing:
            return None

        password_hash = await hash_password(user_data.password)
        user = await self.repository.create(
            user_email=user_data.email,
            hashed_password=password_hash
        )
        return user

    async def authenticate(self, email: str, password: str) -> Optional[Users]:
        user = await self.repository.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def get_by_email(self, email: str) -> Optional[Users]:
        return await self.repository.get_by_email(email)