import os
from dotenv import load_dotenv
from pathlib import Path

from pydantic_settings import BaseSettings

load_dotenv()

BaseDir = Path(__file__).parent.parent

POSTGRES_HOST: str = os.getenv('POSTGRES_HOST')
POSTGRES_PORT: str = os.getenv('POSTGRES_PORT')
POSTGRES_USER: str = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB: str = os.getenv('POSTGRES_DB')
RABBITMQ_HOST: str = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER: str = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD: str = os.getenv('RABBITMQ_PASSWORD')
REDIS_HOST: str = os.getenv('REDIS_HOST')

ACCESS_TOKEN_EXPIRE_MIN = os.getenv('ACCESS_TOKEN_EXPIRE_MIN')
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv('REFRESH_TOKEN_EXPIRE_DAYS')


class JWTSettings(BaseSettings):
    private_key_path: Path = BaseDir / "certificates" / "private_key.pem"
    public_key_path: Path = BaseDir / "certificates" / "public_key.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = int(ACCESS_TOKEN_EXPIRE_MIN)
    refresh_token_expire_days: int = int(REFRESH_TOKEN_EXPIRE_DAYS)


class Settings(BaseSettings):
    POSTGRES_HOST: str = POSTGRES_HOST
    POSTGRES_PORT: str = POSTGRES_PORT
    POSTGRES_USER: str = POSTGRES_USER
    POSTGRES_PASSWORD: str = POSTGRES_PASSWORD
    POSTGRES_DB: str = POSTGRES_DB

    RABBITMQ_HOST: str = RABBITMQ_HOST
    RABBITMQ_USER: str = RABBITMQ_USER
    RABBITMQ_PASSWORD: str = RABBITMQ_PASSWORD

    REDIS_HOST: str = REDIS_HOST

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}?async_fallback=True"

    db_echo: bool = False
    auth_jwt: JWTSettings = JWTSettings()


settings = Settings()
