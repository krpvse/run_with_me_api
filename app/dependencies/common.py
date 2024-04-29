from fastapi import Request, HTTPException

from app.dependencies.base import Dependencies
from app.exceptions.exceptions import NoPermissionsException


async def disallow_without_owner_permissions(request: Request):
    d = Dependencies(request)
    profile_id = d.get_profile_id()
    current_user = await d.get_current_user()

    if profile_id != current_user.id:
        raise NoPermissionsException


async def check_owner_permissions(request: Request):
    d = Dependencies(request)

    try:
        profile_id = d.get_profile_id()
        current_user = await d.get_current_user()
    except HTTPException:
        return False

    if profile_id and current_user and profile_id == current_user.id:
        return True
    else:
        return False
