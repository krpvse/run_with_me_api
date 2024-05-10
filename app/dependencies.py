from fastapi import Depends, Request

from app.auth.router import update_jwt_cookies_depends_on_refresh_token
from app.auth.token import decode_jwt
from app.exceptions.exceptions import NoParamException, NoPermissionsException


def get_profile_id_from_path_params(request: Request):
    profile_id = request.path_params.get('profile_id')
    if not profile_id:
        raise NoParamException
    return int(profile_id) if profile_id else None


async def disallow_without_owner_permissions(
        profile_id: int = Depends(get_profile_id_from_path_params),
        response: dict = Depends(update_jwt_cookies_depends_on_refresh_token)
):
    access_token = response.get('access_token')
    payload = decode_jwt(access_token)
    current_user_id = int(payload.get('sub'))
    if profile_id != current_user_id:
        raise NoPermissionsException
