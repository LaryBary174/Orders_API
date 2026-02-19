from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, status, HTTPException

from core.dependencies import get_current_user
from schemas.user_schema import UserCheck, UserCreate
from database.db import db_engine
from jwt_auth.authjwt import create_access_token
from services.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(
        session: AsyncSession = Depends(db_engine.session_dependency)
) -> UserService:
    return UserService(session)


@router.post(
    "/register",
    response_model=UserCheck,
    status_code=status.HTTP_201_CREATED,
)
async def register(
        user: UserCreate,
        user_service: UserService = Depends(get_user_service)
):
    user = await user_service.register(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )
    return user


@router.post("/token")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(get_user_service)
):
    user = await user_service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
        )
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_access_token({"sub": user.email})

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
    }


@router.get("/me", response_model=UserCheck)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user