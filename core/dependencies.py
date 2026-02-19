from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import db_engine
from database.models import Users
from jwt_auth.authjwt import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_engine.session_dependency)
) -> Users:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise credentials_exception

        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    query = select(Users).where(Users.email == email)
    result = await session.execute(query)
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user