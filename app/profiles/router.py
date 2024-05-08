from fastapi import APIRouter, UploadFile, Depends

from app.profiles.schemas import SProfile, SCoords
from app.profiles.dao import UsersDAO, RunnersDAO, CoordinatesDAO
from app.profiles.dto import ProfileInfoDTO
from app.dependencies import disallow_without_owner_permissions
from app.exceptions.exceptions import UserDoesNotExistException, UnknownAPIException
from app.files.images import download_image
from app.files.files import delete_file


router = APIRouter(
    prefix='/api/profiles',
    tags=['Profiles']
)


@router.get('/id{profile_id}')
async def get_profile_info(profile_id: int) -> ProfileInfoDTO:
    profile_info = await UsersDAO.get_user_info(user_id=profile_id)
    if not profile_info:
        raise UserDoesNotExistException
    return profile_info


@router.post('/id{profile_id}/edit', dependencies=[Depends(disallow_without_owner_permissions)])
async def edit_profile(profile_id: int, update_data: SProfile):
    updated_ids = await RunnersDAO.update(update_data=update_data.dict(), user_id=profile_id)
    if not updated_ids:
        raise UnknownAPIException
    return {'msg': 'Profile is updated', 'profile_id': profile_id}


@router.post('/id{profile_id}/download-image', dependencies=[Depends(disallow_without_owner_permissions)])
async def download_profile_image(profile_id: int, file: UploadFile):
    download_image(
        path=f'app/static/images/profile-images/profile{profile_id}.webp',
        file=file.file
    )
    return {'msg': 'Profile image is downloaded', 'profile_id': profile_id}


@router.delete('/id{profile_id}/delete-image', dependencies=[Depends(disallow_without_owner_permissions)])
async def delete_profile_image(profile_id: int):
    delete_file(f'app/static/images/profile-images/profile{profile_id}.webp')
    return {'msg': 'Profile image is deleted', 'profile_id': profile_id}


@router.get('/id{profile_id}/coordinates')
async def get_coordinates(profile_id: int):
    user = await UsersDAO.find_one_or_none(id=profile_id)
    if not user:
        raise UserDoesNotExistException
    coordinates = await CoordinatesDAO.get_coordinates(runner_id=profile_id)
    return {'profile_id': profile_id, 'coordinates': coordinates}


@router.post('/id{profile_id}/coordinates/add', dependencies=[Depends(disallow_without_owner_permissions)])
async def add_coordinates(profile_id: int, data: SCoords):
    new_id = await CoordinatesDAO.add_one(runner_id=profile_id, latitude=data.latitude, longitude=data.longitude)
    if not new_id:
        raise UnknownAPIException
    return {
        'msg': 'Coordinates is added',
        'coordinates_id': new_id,
        'latitude': data.latitude,
        'longitude': data.longitude,
        'profile_id': profile_id
    }


@router.delete('/id{profile_id}/coordinates/delete', dependencies=[Depends(disallow_without_owner_permissions)])
async def delete_coordinates(profile_id: int, coordinates_id: int):
    deleted_ids = await CoordinatesDAO.delete(runner_id=profile_id, id=coordinates_id)
    if not deleted_ids:
        raise UnknownAPIException
    return {'msg': 'Coordinates is deleted',  'deleted_ids': deleted_ids, 'profile_id': profile_id}
