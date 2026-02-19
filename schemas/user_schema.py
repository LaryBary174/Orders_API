import re

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def password_must_have_letters_and_digits(cls, v: str) -> str:
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Пароль должен содедать хотябы одну букву")
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содедать хотябы одну цифру")
        return v


class UserCheck(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")
