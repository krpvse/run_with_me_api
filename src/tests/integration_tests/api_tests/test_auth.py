import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('name,email,password1,password2,status_code', [
    # positive
    ('Leonid', 'leonid@gmail.com', 'Leonid123', 'Leonid123', 200),

    # negative - existing user
    ('Sergey', 'karpov.important@gmail.com', 'Karpov123', 'Karpov123', 409),
    ('Inna', 'sidorova@example.ru', 'InnaSid2222', 'InnaSid2222', 409),
    ('Ivan', 'sigarev@example.com', 'sigareVV333', 'sigareVV333', 409),

    # negative - name validation
    ('', 'test@gmail.com', 'Test123', 'Test123', 422),
    (None, 'test@gmail.com', 'Test123', 'Test123', 422),
    (123, 'test@gmail.com', 'Test123', 'Test123', 422),

    # negative - email validation
    ('Test', '', 'Test123', 'Test123', 422),
    ('Test', 'good', 'Test123', 'Test123', 422),
    ('Test', 123, 'Test123', 'Test123', 422),
    ('Test', None, 'Test123', 'Test123', 422),

    # negative - passwords validation
    ('Test', 'test@gmail.com', 'test123', 'test123', 422),
    ('Test', 'test@gmail.com', '', '', 422),
    ('Test', 'test@gmail.com', 0, 0, 422),
    ('Test', 'test@gmail.com', 'test', 'test', 422),
    ('Test', 'test@gmail.com', 'Test', 'Test', 422),
    ('Test', 'test@gmail.com', 'TEST123!', '321Test321', 422),
])
async def test_register(name, email, password1, password2, status_code, ac: AsyncClient):
    response = await ac.post('/api/auth/register', json={
        'name': name,
        'email': email,
        'password1': password1,
        'password2': password2
    })
    assert response.status_code == status_code


@pytest.mark.parametrize('email,password1,status_code', [
    # positive - confirmed email
    ('karpov.important@gmail.com', 'Karpov123', 200),

    # negative - unconfirmed email
    ('sidorova@example.ru', 'InnaSid2222', 400),
    ('sigarev@example.com', 'sigareVV333', 400),

    # negative - wrong email or password
    ('karpov@gmail.com', 'Karpov123ERROR', 401),
    ('sidorovERRORa@yandex.ru', 'InnaSid2222', 401),
])
async def test_login(email, password1, status_code, ac: AsyncClient):
    response = await ac.post('/api/auth/login', json={
        'email': email,
        'password1': password1,
    })
    assert response.status_code == status_code


# positive - logout authenticated user
async def test_logout_authenticated(authenticated_ac: AsyncClient):
    assert authenticated_ac.cookies.get('access_token')
    assert authenticated_ac.cookies.get('refresh_token')

    response = await authenticated_ac.post('/api/auth/logout')

    assert response.status_code == 200
    assert authenticated_ac.cookies.get('access_token') is None
    assert authenticated_ac.cookies.get('refresh_token') is None


# positive - logout unauthenticated user
async def test_logout_unauthenticated(ac: AsyncClient):
    response = await ac.post('/api/auth/logout')
    assert response.status_code == 200
    assert ac.cookies.get('access_token') is None
