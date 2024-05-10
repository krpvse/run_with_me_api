import pytest
import sqlalchemy

from app.profiles.dao import RunnersDAO, UsersDAO


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
    {'id': 10, 'email': 'test321@gmail.com',
     'hashed_password': '$2b$12$ppguFcWTS5FkBudp2cVre.HgBNhAGHQ1/kSh82/InCFihswFFlr2q'},
])
async def test_add_positive(data):
    user_id = await UsersDAO.add(**data)
    assert user_id == data['id']

    user = await UsersDAO.find_one_or_none(id=user_id)
    assert user.email == data['email']


@pytest.mark.parametrize('data', [
    # negative - already exist (primary/unique constraints)
    {'id': 1, 'email': 'another@gmail.com',
     'hashed_password': '$2b$12$ppguFcWTS5FkBudp2cVre.HgBNhAGHQ1/kSh82/InCFihswFFlr2q'},

    # negative - not enough values
    {'id': 15},
])
async def test_add_negative(data):
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await UsersDAO.add(**data)


@pytest.mark.parametrize('filter_by,update_data,is_changed', [
    # positive
    ({'user_id': 1}, {'name': 'Success Test Update Name', 'age': 35}, True),
    ({'user_id': 1}, {'age': None}, True),
])
async def test_update_positive(filter_by, update_data, is_changed):
    data_before = await RunnersDAO.find_one_or_none(**filter_by)
    await RunnersDAO.update(update_data, **filter_by)
    data_after = await RunnersDAO.find_one_or_none(**filter_by)

    assert is_changed == (data_before != data_after)
    if is_changed:
        for k, v in update_data.items():
            assert k in data_after.__dict__
            assert data_after.__dict__[k] == v


@pytest.mark.parametrize('filter_by,update_data,exception_type', [
    # negative -  key does not exist
    ({'user_id': 1}, {'wrong_key': 'wrong_value'}, sqlalchemy.exc.CompileError),

    # negative - constraints
    ({'user_id': 1}, {'name': None}, sqlalchemy.exc.IntegrityError),
])
async def test_update_negative(filter_by, update_data, exception_type):
    with pytest.raises(exception_type):
        await RunnersDAO.update(update_data, **filter_by)
