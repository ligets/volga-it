import asyncio
import uuid
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.authentication.utils import get_password_hash, is_valid_password
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


async def seeder_db():
    async with async_session_maker() as session:
        await session.execute(text("""
                INSERT INTO roles (name) VALUES
                    ('Admin'),
                    ('Manager'),
                    ('Doctor'),
                    ('User')
            """))

        admin_hash_password = get_password_hash('admin')
        manager_hash_password = get_password_hash('manager')
        doctor_hash_password = get_password_hash('doctor')
        user_hash_password = get_password_hash('user')

        await session.execute(
            text(f"""
                    INSERT INTO users (id, "username", "firstName", "lastName", "hashed_password", "is_deleted") VALUES
                    ('{uuid.uuid4()}', 'admin', 'Иван', 'Иванов', '{admin_hash_password}', FALSE),
                    ('{uuid.uuid4()}', 'manager', 'Василий', 'Васильев', '{manager_hash_password}', FALSE),
                    ('{uuid.uuid4()}', 'doctor', 'Михаил', 'Михайлов', '{doctor_hash_password}', FALSE),
                    ('{uuid.uuid4()}', 'user', 'Петр', 'Петров', '{user_hash_password}', FALSE),
                    ('{uuid.uuid4()}', 'asd', 'Петр', 'Петров', '{user_hash_password}', FALSE)
                """)
        )

        user_ids = (await session.execute(
            text("""
                        SELECT id, username FROM users WHERE username IN ('admin', 'manager', 'doctor', 'user')
                    """)
        )).fetchall()

        # Получаем id ролей
        role_ids = (await session.execute(
            text("""
                        SELECT id, name FROM roles WHERE name IN ('Admin', 'Manager', 'Doctor', 'User')
                    """)
        )).fetchall()

        user_role_mapping = {
            'admin': 'Admin',
            'manager': 'Manager',
            'doctor': 'Doctor',
            'user': 'User',
            'asd': 'User'
        }

        for user_id, username in user_ids:
            role_id = next(role_id for role_id, role_name in role_ids if role_name == user_role_mapping[username])
            await session.execute(
                text(f"""
                            INSERT INTO user_mtm_role (user_id, role_id) VALUES ('{user_id}', '{role_id}')
                        """)
            )

        await session.commit()
    

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await seeder_db()
    yield
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(params=[
    {"username": "admin", "password": "admin"},
    {"username": "manager", "password": "manager"},
    {"username": "doctor", "password": "doctor"},
    {"username": "user", "password": "user"},
])
async def users_data(request, ac: AsyncClient):
    user_data = request.param
    username = user_data["username"]
    password = user_data["password"]

    response = await ac.post('/api/Authentication/SignIn', json={
        "username": username,
        "password": password
    })

    assert response.status_code == 200, f'{response.json()}'
    token = response.json()['access_token']
    return {
        'username': username,
        'token': token
    }
