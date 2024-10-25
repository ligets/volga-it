from dotenv import load_dotenv
from pathlib import Path

import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

BaseDir = Path(__file__).parent.parent


class JWTSettings(BaseSettings):
    private_key_path: Path = BaseDir / "certificates" / "private_key.pem"
    public_key_path: Path = BaseDir / "certificates" / "public_key.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    model_config = SettingsConfigDict(env_file='.env', extra='ignore', env_prefix='JWT_')


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    POSTGRES_TEST_HOST: str
    POSTGRES_TEST_PORT: str
    POSTGRES_TEST_USER: str
    POSTGRES_TEST_PASSWORD: str
    POSTGRES_TEST_DB: str

    RABBITMQ_HOST: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    # REDIS_HOST: str

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def POSTGRES_TEST_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_TEST_USER}:{self.POSTGRES_TEST_PASSWORD}@{self.POSTGRES_TEST_HOST}:{self.POSTGRES_TEST_PORT}/{self.POSTGRES_TEST_DB}"

    db_echo: bool = False
    auth_jwt: JWTSettings = JWTSettings()

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()

logger = logging.getLogger("uvicorn.error")
