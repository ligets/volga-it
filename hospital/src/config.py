from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

load_dotenv()


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

    # AUTH_HOST: str

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def POSTGRES_TEST_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_TEST_USER}:{self.POSTGRES_TEST_PASSWORD}@{self.POSTGRES_TEST_HOST}:{self.POSTGRES_TEST_PORT}/{self.POSTGRES_TEST_DB}"

    db_echo: bool = False

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()


logger = logging.getLogger("uvicorn.error")
