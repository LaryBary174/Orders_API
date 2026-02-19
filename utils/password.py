import asyncio
from passlib.context import CryptContext

context = CryptContext(schemes=["argon2"], deprecated="auto")


async def hash_password(password: str) -> str:
    """Хэшировать пароль с использованием argon2."""
    return await asyncio.to_thread(context.hash, password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль на соответствие хэшу."""
    return context.verify(plain_password, hashed_password)
