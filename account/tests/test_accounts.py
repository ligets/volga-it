from httpx import AsyncClient
from sqlalchemy import text

from tests.conftest import async_session_maker


async def test_me(ac: AsyncClient):
    response = await ac.post("/api/Authentication/SignIn", json={"username": "admin", "password": "admin"})
    token = response.json()["access_token"]
    response = await ac.get("/api/Accounts/Me", headers={
        "Authorization": f"Bearer {token}"
    })
    data = response.json()
    assert response.status_code == 200


async def test_update(ac: AsyncClient):
    response = await ac.post("/api/Authentication/SignIn", json={"username": "admin", "password": "admin"})
    token = response.json()["access_token"]
    response = await ac.put("/api/Accounts/Update", json={
        "firstName": "new_name",
        "lastName": "new_name",
        "password": "admin"
    }, headers={
        "Authorization": f"Bearer {token}"
    })
    data = response.json()
    assert response.status_code == 200
    assert data["firstName"] == "new_name"


async def test_get_accounts(ac: AsyncClient, users_data: dict):
    statuses = {
        'admin': 200,
        'manager': 403,
        'doctor': 403,
        'user': 403
    }

    response = await ac.get('/api/Accounts', params={
        'from': 0,
        'count': 10
    }, headers={
        "Authorization": f"Bearer {users_data['token']}"
    })

    assert response.status_code == statuses[users_data['username']]


async def test_post_accounts(ac: AsyncClient, users_data):
    statuses = {
        'admin': 200,
        'manager': 403,
        'doctor': 403,
        'user': 403
    }

    response = await ac.post('/api/Accounts', json={
        "firstName": "string",
        "lastName": "string",
        "username": "string",
        "password": "string",
        "roles": [
            "string"
        ]
    }, headers={
        "Authorization": f"Bearer {users_data['token']}"
    })

    assert response.status_code == statuses[users_data['username']]


async def test_put_accounts(ac: AsyncClient, users_data):
    statuses = {
        'admin': 200,
        'manager': 403,
        'doctor': 403,
        'user': 403
    }
    async with async_session_maker() as session:
        res = await session.execute(text('''
            SELECT * FROM users WHERE username = :username
        '''), {'username': 'asd'})
        user = res.mappings().one_or_none()

    response = await ac.put(f'/api/Accounts/{user.id}', json={
        "firstName": "new_name",
        "lastName": "new_name",
        "password": user.username,
        "username": user.username,
        "roles": [
            'User'
        ]
    }, headers={
        "Authorization": f"Bearer {users_data['token']}"
    })

    assert response.status_code == statuses[users_data['username']]


async def test_delete_accounts(ac: AsyncClient, users_data):
    statuses = {
        'admin': 200,
        'manager': 403,
        'doctor': 403,
        'user': 403
    }

    async with async_session_maker() as session:
        res = await session.execute(text('''
            SELECT * FROM users WHERE username = :username
        '''), {'username': 'asd'})
        user = res.mappings().one_or_none()

    response = await ac.delete(f'/api/Accounts/{user.id}', headers={
        "Authorization": f"Bearer {users_data['token']}"
    })

    assert response.status_code == statuses[users_data['username']]





