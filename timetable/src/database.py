from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(
            url=url, echo=echo
        )

        self.session = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            bind=self.engine
        )

    async def get_async_session(self):
        async with self.session() as session:
            yield session
            await session.commit()


db = DatabaseHelper(
    url=settings.POSTGRES_URL,
    echo=settings.db_echo
)
