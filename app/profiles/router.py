import shutil

from fastapi import APIRouter, UploadFile, Depends

from app.profiles.schemas import SProfile
from app.profiles.dao import UsersDAO, RunnersDAO
from app.dependencies.common import disallow_without_owner_permissions
from app.exceptions.exceptions import UserDoesNotExistException


router = APIRouter(
    prefix='/api/profiles',
    tags=['Profiles']
)


@router.get('/{profile_id}')
async def get_profile_info(profile_id: int):
    profile_info = await UsersDAO.get_user_info(user_id=profile_id)
    if not profile_info:
        raise UserDoesNotExistException
    return profile_info


@router.post('/edit-profile/{profile_id}', dependencies=[Depends(disallow_without_owner_permissions)])
async def edit_profile(profile_id: int, update_data: SProfile):
    user = await UsersDAO.find_one_or_none(id=profile_id)
    if not user:
        raise UserDoesNotExistException
    await RunnersDAO.update(update_data=update_data.dict(), user_id=profile_id)
    return {'msg': 'Success! Profile is updated', 'profile_id': profile_id}


@router.post('/download-profile-image/{profile_id}', dependencies=[Depends(disallow_without_owner_permissions)])
async def download_profile_image(profile_id: int, file: UploadFile):
    with open(f'app/static/images/profile-images/profile{profile_id}.webp', 'wb+') as file_obj:
        shutil.copyfileobj(file.file, file_obj)
    return {'msg': 'Success! Profile images is downloaded', 'profile_id': profile_id}
