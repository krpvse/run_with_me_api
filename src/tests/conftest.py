import asyncio
import json

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from src.database import Base, engine, session_maker
from src.main import app as fastapi_app
from src.profiles.models import Coordinates, Runners, Users
from src.settings import settings


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'src/tests/mock_data/mock_{model}.json', encoding='utf-8') as file:
            return json.load(file)

    users = open_mock_json('users')
    runners = open_mock_json('runners')
    coordinates = open_mock_json('coordinates')

    async with session_maker() as session:
        add_users = insert(Users).values(users)
        add_runners = insert(Runners).values(runners)
        add_coordinates = insert(Coordinates).values(coordinates)

        await session.execute(add_users)
        await session.execute(add_runners)
        await session.execute(add_coordinates)

        await session.commit()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='function')
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        response = await ac.post('/api/auth/login', json={
            'email': 'karpov.important@gmail.com',
            'password1': 'Karpov123',
        })
        assert response.status_code == 200
        assert ac.cookies.get('access_token')
        assert ac.cookies.get('refresh_token')
        yield ac


@pytest.fixture(scope='session')
def event_loop(request):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop
    loop.close()
