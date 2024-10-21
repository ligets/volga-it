from httpx import AsyncClient
from sqlalchemy import text

from tests.pytest.conftest import async_session_maker


async def test_get_list_doctors(ac: AsyncClient):
    response = await ac.post("/api/Authentication/SignIn", json={"username": "user", "password": "user"})
    token = response.json()["access_token"]
    response = await ac.get('/api/Doctors', params={
        'nameFilter': '',
        'from': 0,
        'count': 10
    }, headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200


async def test_get_doctor(ac: AsyncClient):
    response = await ac.post("/api/Authentication/SignIn", json={"username": "user", "password": "user"})
    token = response.json()["access_token"]
    async with async_session_maker() as session:
        res = await session.execute(text('''
            SELECT * FROM users WHERE username = :username
        '''), {'username': 'doctor'})
        user = res.mappings().one_or_none()

    response = await ac.get(f'/api/Doctors/{user.id}', headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
