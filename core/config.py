from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    JWT_PRIVATE_KEY_PATH: str
    JWT_PUBLIC_KEY_PATH: str

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    RATE_LIMIT_DEFAULT: str = "4/minute"

    REDIS_URL: str = "redis://redis:6379/0"
    BROKER_URL: str = "amqp://guest:guest@rabbitmq:5672//"

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

    def _read_key(self, path: str) -> str:
        key_path = Path(path)
        return key_path.read_text()

    @property
    def private_key(self):
        return self._read_key(self.JWT_PRIVATE_KEY_PATH)

    @property
    def public_key(self):
        return self._read_key(self.JWT_PUBLIC_KEY_PATH)


settings = Settings()
