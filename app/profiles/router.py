import shutil

from fastapi import APIRouter, UploadFile, Depends

from app.profiles.schemas import SProfile
from app.profiles.services import UsersService, RunnersService
from app.dependencies.common import disallow_without_owner_permissions
from app.exceptions import UserDoesNotExistsException


router = APIRouter(
    prefix='/api/profiles',
    tags=['Profiles']
)


@router.get('/{profile_id}')
async def get_profile_info(profile_id: int):
    profile_info = await UsersService.get_user_info(user_id=profile_id)
    if not profile_info:
        raise UserDoesNotExistsException
    return profile_info


@router.post('/edit-profile/{profile_id}', dependencies=[Depends(disallow_without_owner_permissions)])
async def edit_profile(profile_id: int, update_data: SProfile):
    user = await UsersService.find_one_or_none(id=profile_id)
    if not user:
        raise UserDoesNotExistsException
    await RunnersService.update_profile(user_id=profile_id, update_data=update_data)


@router.post('/download-profile-image/{profile_id}', dependencies=[Depends(disallow_without_owner_permissions)])
async def download_profile_image(profile_id: int, file: UploadFile):
    with open(f'app/static/images/profile-images/profile{profile_id}.webp', 'wb+') as file_obj:
        shutil.copyfileobj(file.file, file_obj)