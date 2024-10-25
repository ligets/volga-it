from httpx import AsyncClient
from sqlalchemy import text

from src.accounts.dao import UserDAO
from tests.pytest.conftest import async_session_maker

login_data = {}


async def test_register(ac: AsyncClient):
    response = await ac.post('/api/Authentication/SignUp', json={
        "firstName": "test_user",
        "lastName": "test_user",
        "username": "test_user",
        "password": "test_user"
    })
    data = response.json()

    assert response.status_code == 200, f'Другой статус - {data}'
    assert 'access_token' in response.json(), 'Нету access_token в response'
    assert 'refresh_token' in response.json(), 'Нету refresh_token в response'


async def test_login(ac: AsyncClient):
    global login_data
    response = await ac.post('/api/Authentication/SignIn', json={
        'username': 'test_user',
        'password': 'test_user'
    })
    login_data = response.json()

    assert response.status_code == 200, f'Другой статус - {login_data}'
    assert 'access_token' in login_data, 'Нету access_token в response'
    assert 'refresh_token' in login_data, 'Нету refresh_token в response'


async def test_refresh(ac: AsyncClient):
    global login_data
    response = await ac.post('/api/Authentication/Refresh', json={
        'refreshToken': login_data['refresh_token']
    })
    data = response.json()

    assert response.status_code == 200, f'Другой статус - {data}'
    assert 'access_token' in data, 'Нету access_token в response'
    assert 'refresh_token' in data, 'Нету refresh_token в response'


async def test_logout(ac: AsyncClient):
    global login_data
    response = await ac.put('/api/Authentication/SignOut', headers={
        'Authorization': f'Bearer {login_data["access_token"]}'
    })
    data = response.json()

    assert response.status_code == 200, f'Другой статус - {data}'


async def test_fail_login(ac: AsyncClient):
    response = await ac.post('/api/Authentication/SignIn', json={
        'username': 'test_user',
        'password': 'fail_user'
    })
    data = response.json()

    assert response.status_code == 401, f'Другой статус - {data}'
    assert 'detail' in data, 'Нету detail в response'
    assert data['detail'] == 'Invalid username or password.', 'Другая ошибка'


async def test_repeat_username(ac: AsyncClient):
    response = await ac.post('/api/Authentication/SignUp', json={
        "firstName": "test_user",
        "lastName": "test_user",
        "username": "test_user",
        "password": "test_user"
    })
    data = response.json()

    assert response.status_code == 409, f'Другой статус - {data}'
    assert 'detail' in data, 'Нету detail в response'
    assert data['detail'] == 'Username is already taken.', f'Другая ошибка - {data["detail"]}'


async def test_repeat_refresh(ac: AsyncClient):
    global login_data
    response = await ac.post('/api/Authentication/Refresh', json={
        'refreshToken': login_data['refresh_token']
    })
    data = response.json()

    assert response.status_code == 401, f'Другой статус - {data}'
    assert 'detail' in data, 'Нету detail в response'
    assert data['detail'] == 'Invalid token.', f'Другая ошибка - {data["detail"]}'




