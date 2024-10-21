from httpx import AsyncClient
from sqlalchemy import text

from tests.conftest import async_session_maker


async def test_create_hospital(ac: AsyncClient, users_data: dict):
    data = {
        "name": "test",
        "address": "test",
        "contactPhone": "1234567890",
        "rooms": [
            "test1",
            "test2"
        ]
    }
    statuses = {
        'admin': 200,
        'manager': 403,
        'doctor': 403,
        'user': 403
    }

    response = await ac.post("/api/Hospitals", json=data, headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })
    assert response.status_code == statuses[users_data['username']]


async def test_get_list_hospitals(ac: AsyncClient):
    async with AsyncClient() as lac:
        response = await lac.post('http://localhost:8081/api/Authentication/SignIn', json={
            "username": 'user',
            "password": 'user'
        })
        data = response.json()

    response = await ac.get('/api/Hospitals', params={
        'from': 0,
        'count': 10
    }, headers={
        'Authorization': f'Bearer {data["access_token"]}'
    })
    assert response.status_code == 200, f'Другой статус - {response.json()}'
    assert len(response.json()) <= 10, 'Количество не совпадает'


async def test_get_hospital(ac: AsyncClient):
    async with AsyncClient() as lac:
        response = await lac.post('http://localhost:8081/api/Authentication/SignIn', json={
            "username": 'user',
            "password": 'user'
        })
        data = response.json()

    async with async_session_maker() as session:
        res = await session.execute(text("""
            SELECT * FROM hospitals
        """))
        hospital = res.mappings().first()
    response = await ac.get(f'/api/Hospitals/{hospital.id}', headers={
        'Authorization': f'Bearer {data["access_token"]}'
    })
    assert response.status_code == 200, f'Другой статус - {response.json()}'
    assert 'id' in response.json()
    assert 'name' in response.json()
    assert 'address' in response.json()
    assert 'contactPhone' in response.json()


async def test_put_hospitals(ac: AsyncClient, users_data: dict):
    data = {
        "name": "new",
        "address": "new",
        "contactPhone": "new",
        "rooms": [
            "new",
            "test2"
        ]
    }
    statuses = {
        'admin': 200,
        'manager': 403,
        'doctor': 403,
        'user': 403
    }

    response = await ac.get("/api/Hospitals", params={
        'from': 0,
        'count': 10
    }, headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })
    assert response.status_code == 200
    old_hospital = response.json()[0]

    response = await ac.put(f"/api/Hospitals/{old_hospital['id']}", json=data, headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })
    assert response.status_code == statuses[users_data['username']]


async def test_get_list_room_hospital(ac: AsyncClient):
    async with AsyncClient() as lac:
        response = await lac.post('http://localhost:8081/api/Authentication/SignIn', json={
            "username": 'user',
            "password": 'user'
        })
        data = response.json()
    async with async_session_maker() as session:
        res = await session.execute(text("""
            SELECT * FROM hospitals
        """))
        hospital = res.mappings().first()
    response = await ac.get(f'/api/Hospitals/{hospital.id}/Rooms', headers={
        'Authorization': f'Bearer {data["access_token"]}'
    })
    assert response.status_code == 200, f'Другой статус - {response.json()}'
    for i in response.json():
        assert i['name'] in ["new", "test2"]


async def test_delete_hospital(ac: AsyncClient, users_data: dict):
    statuses = {
        'admin': 200,
        'manager': 403,
        'doctor': 403,
        'user': 403
    }

    response = await ac.get("/api/Hospitals", params={
        'from': 0,
        'count': 10
    }, headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })
    assert response.status_code == 200
    hospital = response.json()[0]

    response = await ac.delete(f"/api/Hospitals/{hospital['id']}", headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })
    assert response.status_code == statuses[users_data['username']]
    if response.status_code == 200:
        response = await ac.get(f"/api/Hospitals/{hospital['id']}", headers={
            'Authorization': f'Bearer {users_data["token"]}'
        })
        assert response.status_code == 404, f'Другой статус - {response.json()}'






