from datetime import datetime, timedelta, timezone

from jose import jwt
from core.config import settings

ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
REFRESH_TOKEN_EXPIRE = timedelta(days=7)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire, "type": "access"})
    key = settings.private_key
    return jwt.encode(to_encode, key, algorithm="RS256")


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or REFRESH_TOKEN_EXPIRE)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.private_key, algorithm="RS256")


def decode_token(token: str) -> dict:
    key = settings.public_key
    return jwt.decode(token, key, algorithms=["RS256"])
