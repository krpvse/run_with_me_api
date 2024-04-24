import pytest
import sqlalchemy

from app.profiles.dao import UsersDAO


@pytest.mark.parametrize('filter_by,is_present', [
    # positive
    ({'id': 2}, True),
    ({'email': 'sidorova@yandex.ru'}, True),

    # negative - not existing
    ({'id': 900}, False),
])
async def test_find_one_or_none(filter_by, is_present):
    user = await UsersDAO.find_one_or_none(**filter_by)
    assert bool(user) == is_present
    if user:
        assert user.id == 2
        assert user.email == 'sidorova@yandex.ru'


@pytest.mark.parametrize('data', [
    # positive
    {'id': 10, 'email': 'test321@gmail.com', 'hashed_password': '$2b$12$ppguFcWTS5FkBudp2cVre.HgBNhAGHQ1/kSh82/InCFihswFFlr2q'},
])
async def test_add_positive(data):
    user_id = await UsersDAO.add(**data)
    assert user_id == data['id']

    user = await UsersDAO.find_one_or_none(id=user_id)
    assert user.email == data['email']


@pytest.mark.parametrize('data', [
    # negative - already exist (primary/unique constraints)
    {'id': 1, 'email': 'another@gmail.com', 'hashed_password': '$2b$12$ppguFcWTS5FkBudp2cVre.HgBNhAGHQ1/kSh82/InCFihswFFlr2q'},

    # negative - not enough values
    {'id': 15},
])
async def test_add_negative(data):
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await UsersDAO.add(**data)
