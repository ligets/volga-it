import asyncio
import uuid
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.database import db
from src.base_model import Base
from src.config import settings
from src.main import app

engine_test = create_async_engine(settings.POSTGRES_TEST_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.commit()


app.dependency_overrides[db.get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(params=[
    {"username": "admin", "password": "admin"},
    {"username": "manager", "password": "manager"},
    {"username": "doctor", "password": "doctor"},
    {"username": "user", "password": "user"},
])
async def users_data(request):
    user_data = request.param
    username = user_data["username"]
    password = user_data["password"]

    async with AsyncClient() as ac:
        response = await ac.post('http://localhost:8081/api/Authentication/SignIn', json={
            "username": username,
            "password": password
        })

    assert response.status_code == 200, f'{response.json()}'
    token = response.json()['access_token']
    return {
        'username': username,
        'token': token
    }
