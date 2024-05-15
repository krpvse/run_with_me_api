import pytest
from httpx import AsyncClient

from src.profiles.dao import UsersDAO


@pytest.mark.parametrize('profile_id, status_code', [
    # positive
    (1, 200),
    (2, 200),
    (3, 200),

    # negative
    (0, 400),
    (999, 400),
    (None, 422),
    ('SomeText', 422),
])
async def test_get_profile_info(profile_id, status_code, ac: AsyncClient):
    response = await ac.get(f'api/profiles/id{profile_id}')

    assert response.status_code == status_code
    if response.status_code == 200:
        profile = await UsersDAO.get_user_info(user_id=profile_id)
        profile_form_dao = profile.model_dump()
        profile_from_api = response.json()
        assert profile_form_dao == profile_from_api


@pytest.mark.parametrize('profile_id, update_data, is_changed, status_code', [
    # positive
    (1, {'name': 'New Name'}, True, 200),
    (1, {'name': 'New Name', 'age': 10, 'description': 'Cool description'}, True, 200),

    # negative - not existing user
    (999, {'name': 'New Name'}, False, 400),

    # negative - no permissions (because authenticated as user with user_id = 1)
    (2, {'name': 'New Name'}, False, 400),

    # negative - wrong update data
    (1, {}, False, 422),
    (1, {'wrong_key': 'wrong_value'}, False, 422),
    (1, {'name': 999}, False, 422),
    (1, {'name': None}, False, 422),
    (1, {'description': None}, False, 422),
    (1, {'description': 999}, False, 422),
    (1, {'description': 999}, False, 422),
    (1, {'age': 'Text'}, False, 422),
    (1, {'distance_from': 'Text'}, False, 422),
    (1, {'speed_to': 'Text'}, False, 422),
])
async def test_edit_profile(profile_id, update_data, is_changed, status_code, authenticated_ac: AsyncClient):
    profile_before = await UsersDAO.get_user_info(user_id=profile_id)

    response = await authenticated_ac.post(f'api/profiles/id{profile_id}/edit', json=update_data)
    assert response.status_code == status_code

    profile_after = await UsersDAO.get_user_info(user_id=profile_id)
    assert is_changed == (profile_before != profile_after)
