from httpx import AsyncClient
from sqlalchemy import text

from tests.conftest import async_session_maker


async def test_create_timetable(ac: AsyncClient, users_data: dict):
    data = {
        "hospitalId": "fe82a64e-3c26-49b9-b961-7d5fe543fbf6",
        "doctorId": "00527e2e-0183-4e10-8bb6-86a9837a0cba",
        "from": "2024-10-22T18:00:00Z",
        "to": "2024-10-22T20:00:00Z",
        "room": "string"
    }
    statuses = {
        "admin": 200,
        "manager": 200,
        "doctor": 403,
        "user": 403
    }
    response = await ac.post("/api/Timetable", json=data, headers={
        "Authorization": f"Bearer {users_data['token']}"
    })

    assert response.status_code == statuses[users_data['username']]

    return response.json() if response.status_code == 200 else None


async def test_update_timetable(ac: AsyncClient, users_data: dict):
    data = {
        "hospitalId": "fe82a64e-3c26-49b9-b961-7d5fe543fbf6",
        "doctorId": "00527e2e-0183-4e10-8bb6-86a9837a0cba",
        "from": "2024-10-22T12:00:00Z",
        "to": "2024-10-22T20:00:00Z",
        "room": "string"
    }
    statuses = {
        "admin": 200,
        "manager": 200,
        "doctor": 403,
        "user": 403
    }
    async with async_session_maker() as session:
        res = await session.execute(text('''
            SELECT id FROM timetable LIMIT 1
        '''))
        timetable = res.scalars().one_or_none()

    response = await ac.put(f"/api/Timetable/{timetable}", json=data, headers={
        "Authorization": f"Bearer {users_data['token']}"
    })
    assert response.status_code == statuses[users_data['username']]


async def test_get_timetable_hospital(ac: AsyncClient):
    async with AsyncClient() as lac:
        response = await lac.post('http://localhost:8081/api/Authentication/SignIn', json={
            "username": 'user',
            "password": 'user'
        })
        data = response.json()
    response = await ac.get('/api/Timetable/Hospital/fe82a64e-3c26-49b9-b961-7d5fe543fbf6', params={
        "from": "2024-10-22T11:00:00Z",
        "to": "2024-10-22T20:00:00Z",
    }, headers={
        'Authorization': f'Bearer {data["access_token"]}'
    })
    assert response.status_code == 200, f'Другой статус - {response.json()}'
    assert len(response.json()) > 0


async def test_get_timetable_doctor(ac: AsyncClient):
    async with AsyncClient() as lac:
        response = await lac.post('http://localhost:8081/api/Authentication/SignIn', json={
            "username": 'user',
            "password": 'user'
        })
        data = response.json()
    response = await ac.get('/api/Timetable/Doctor/00527e2e-0183-4e10-8bb6-86a9837a0cba', params={
        "from": "2024-10-22T11:00:00Z",
        "to": "2024-10-22T20:00:00Z",
    }, headers={
        'Authorization': f'Bearer {data["access_token"]}'
    })
    assert response.status_code == 200, f'Другой статус - {response.json()}'
    assert len(response.json()) > 0


async def test_get_timetable_room_hospital(ac: AsyncClient, users_data: dict):
    statuses = {
        "admin": 200,
        "manager": 200,
        "doctor": 200,
        "user": 403
    }

    response = await ac.get('/api/Timetable/Hospital/fe82a64e-3c26-49b9-b961-7d5fe543fbf6/Room/string', params={
        "from": "2024-10-22T11:00:00Z",
        "to": "2024-10-22T20:00:00Z"
    }, headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })
    assert response.status_code == statuses[users_data['username']]
    assert len(response.json()) > 0


async def test_get_appointments(ac: AsyncClient):
    async with AsyncClient() as lac:
        response = await lac.post('http://localhost:8081/api/Authentication/SignIn', json={
            "username": 'user',
            "password": 'user'
        })
        data = response.json()
    async with async_session_maker() as session:
        res = await session.execute(text("""
            SELECT * FROM timetable LIMIT 1
        """))
        timetable = res.mappings().first()
    response = await ac.get(f"/api/Timetable/{str(timetable.id)}/Appointments", headers={
        'Authorization': f'Bearer {data["access_token"]}'
    })
    assert response.status_code == 200, f'Другой статус - {response.json()}'
    assert len(response.json()) > 0


async def test_create_appointments(ac: AsyncClient, time: str = "2024-10-22T12:00:00Z"):
    async with AsyncClient() as lac:
        response = await lac.post('http://localhost:8081/api/Authentication/SignIn', json={
            "username": 'user',
            "password": 'user'
        })
        data = response.json()
    async with async_session_maker() as session:
        res = await session.execute(text("""
            SELECT * FROM timetable LIMIT 1
        """))
        timetable = res.mappings().first()

    response = await ac.post(f"/api/Timetable/{str(timetable.id)}/Appointments", json={
        "time": time
    }, headers={
        'Authorization': f'Bearer {data["access_token"]}'
    })
    assert response.status_code == 200, f'Другой статус - {response.json()}'

    return response.json() if response.status_code == 200 else None


async def test_delete_appointments(ac: AsyncClient, users_data: dict):
    appointments = await test_create_appointments(ac, "2024-10-22T12:30:00Z")
    statuses = {
        "admin": 200,
        "manager": 200,
        "doctor": 403,
        "user": 200
    }
    response = await ac.delete(f"/api/Appointment/{appointments.get('id')}", headers={
        'Authorization': f'Bearer {users_data["token"]}'
    })
    assert response.status_code == statuses[users_data['username']], f'Другой статус - {response.json()}'


async def test_delete_timetable(ac: AsyncClient, users_data: dict):
    async with async_session_maker() as session:
        res = await session.execute(text('''
            SELECT id FROM timetable LIMIT 1
        '''))
        timetable = res.scalars().one_or_none()
    statuses = {
        "admin": 200,
        "manager": 200,
        "doctor": 403,
        "user": 403
    }
    response = await ac.delete(f"/api/Timetable/{timetable}", headers={
        "Authorization": f"Bearer {users_data['token']}"
    })
    assert response.status_code == statuses[users_data['username']]
    if response.status_code == 200:
        async with async_session_maker() as session:
            s = await session.execute(text("""
                SELECT * FROM timetable WHERE id = :id
            """), {'id': timetable})
            assert s.mappings().one_or_none() is None


async def test_delete_timetable_doctor(ac: AsyncClient, users_data: dict):
    data = {
        "hospitalId": "fe82a64e-3c26-49b9-b961-7d5fe543fbf6",
        "doctorId": "00527e2e-0183-4e10-8bb6-86a9837a0cba",
        "from": "2024-10-22T18:00:00Z",
        "to": "2024-10-22T20:00:00Z",
        "room": "string"
    }
    statuses = {
        "admin": 200,
        "manager": 200,
        "doctor": 403,
        "user": 403
    }
    response = await ac.post("/api/Timetable", json=data, headers={
        "Authorization": f"Bearer {users_data['token']}"
    })

    assert response.status_code == statuses[users_data['username']]
    timetable = response.json()
    if response.status_code != 200:
        return

    response = await ac.delete(f"/api/Timetable/Doctor/{timetable['doctorId']}", headers={
        "Authorization": f"Bearer {users_data['token']}"
    })
    assert response.status_code == statuses[users_data['username']]
    if response.status_code == 200:
        async with async_session_maker() as session:
            s = await session.execute(text("""
                SELECT * FROM timetable WHERE id = :id
            """), {'id': timetable['id']})
            assert s.mappings().one_or_none() is None


async def test_delete_timetable_hospital(ac: AsyncClient, users_data: dict):
    data = {
        "hospitalId": "fe82a64e-3c26-49b9-b961-7d5fe543fbf6",
        "doctorId": "00527e2e-0183-4e10-8bb6-86a9837a0cba",
        "from": "2024-10-22T18:00:00Z",
        "to": "2024-10-22T20:00:00Z",
        "room": "string"
    }
    statuses = {
        "admin": 200,
        "manager": 200,
        "doctor": 403,
        "user": 403
    }
    response = await ac.post("/api/Timetable", json=data, headers={
        "Authorization": f"Bearer {users_data['token']}"
    })

    assert response.status_code == statuses[users_data['username']]
    timetable = response.json()
    if response.status_code != 200:
        return

    response = await ac.delete(f"/api/Timetable/Hospital/{timetable['hospitalId']}", headers={
        "Authorization": f"Bearer {users_data['token']}"
    })
    assert response.status_code == statuses[users_data['username']]
    if response.status_code == 200:
        async with async_session_maker() as session:
            s = await session.execute(text("""
                SELECT * FROM timetable WHERE id = :id
            """), {'id': timetable['id']})
            assert s.mappings().one_or_none() is None



