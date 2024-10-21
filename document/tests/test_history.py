import uuid
from datetime import datetime, timezone

import pytest
from httpx import AsyncClient
from sqlalchemy import text

from tests.conftest import async_session_maker


async def test_fail_create_history(ac: AsyncClient, users_data):
    data = {
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
        'pacientId': str(uuid.uuid4()),
        'hospitalId': str(uuid.uuid4()),
        'doctorId': str(uuid.uuid4()),
        'room': 'string',
        'data': 'Test',
    }
    statuses = {
        'admin': 404,
        'manager': 404,
        'doctor': 404,
        'user': 403
    }
    errors = {
        'admin': 'Pacient not found',
        'manager': 'Pacient not found',
        'doctor': 'Pacient not found',
        'user': 'Not enough privileges.'
    }

    response = await ac.post('/api/History', json=data, headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })

    assert response.status_code == statuses[users_data['username']]
    assert response.json()['detail'] == errors[users_data['username']]


@pytest.mark.asyncio(loop_scope="session")
async def test_create_history(ac: AsyncClient, users_data: dict):
    data = {
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S') + 'Z',
        'pacientId': "ec2d2201-c746-418d-862c-e7eb6730be89",
        'hospitalId': "fe82a64e-3c26-49b9-b961-7d5fe543fbf6",
        'doctorId': "00527e2e-0183-4e10-8bb6-86a9837a0cba",
        'room': 'string',
        'data': 'Test',
    }
    statuses = {
        'admin': 200,
        'manager': 200,
        'doctor': 200,
        'user': 403
    }
    response = await ac.post('/api/History', json=data, headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })

    assert response.status_code == statuses[users_data['username']]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_acc_history(ac: AsyncClient, users_data: dict):
    statuses = {
        'admin': 403,
        'manager': 403,
        'doctor': 200,
        'user': 200
    }
    response = await ac.get('/api/History/Account/ec2d2201-c746-418d-862c-e7eb6730be89', headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })

    assert response.status_code == statuses[users_data['username']]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_history(ac: AsyncClient, users_data: dict):
    statuses = {
        'admin': 403,
        'manager': 403,
        'doctor': 200,
        'user': 200
    }
    response = await ac.get('/api/History/54299c04-f13c-4602-9770-755bc025866a', headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })

    assert response.status_code == statuses[users_data['username']]


@pytest.mark.asyncio(loop_scope="session")
async def test_update_history(ac: AsyncClient, users_data: dict):
    data = {
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S') + 'Z',
        'pacientId': "ec2d2201-c746-418d-862c-e7eb6730be89",
        'hospitalId': "fe82a64e-3c26-49b9-b961-7d5fe543fbf6",
        'doctorId': "00527e2e-0183-4e10-8bb6-86a9837a0cba",
        'room': 'string',
        'data': 'update_history',
    }
    statuses = {
        'admin': 200,
        'manager': 200,
        'doctor': 200,
        'user': 403
    }

    async with async_session_maker() as session:
        res = await session.execute(text("""
            SELECT id FROM history LIMIT 1
        """))
        history = res.scalars().first()
    response = await ac.put(f'/api/History/{history}', json=data, headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })
    assert response.status_code == statuses[users_data['username']]




