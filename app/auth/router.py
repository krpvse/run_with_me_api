from fastapi import APIRouter, Response

from app.auth.schemas import SUserAuth, SUserReg
from app.auth.auth import get_password_hash, verify_password, create_access_token
from app.auth.dao import UsersDAO, RunnersDAO
from app.exceptions import InvalidEmailOrPasswordException, ExistingUserException


router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)


@router.post('/register')
async def register(user_data: SUserReg):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise ExistingUserException
    hashed_password = get_password_hash(user_data.password1)

    user_id = await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    await RunnersDAO.add(user_id=user_id, name=user_data.name)
    return {'user_id': user_id, 'email': user_data.email, 'name': user_data.name}


@router.post('/login')
async def login(response: Response, user_data: SUserAuth):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if not user or not verify_password(user_data.password1, user.hashed_password):
        raise InvalidEmailOrPasswordException

    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)
    return {'user_id': user.id, 'access_token': access_token}


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
