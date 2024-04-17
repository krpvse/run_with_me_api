from fastapi import APIRouter, HTTPException, status, Response

from app.users.schemas import SUserAuth
from app.users.services import UserService
from app.users.auth import get_password_hash, verify_password, create_access_token


router = APIRouter(
    prefix='/api/auth',
    tags=['Users']
)


@router.post('/register')
async def register(user_data: SUserAuth):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    hashed_password = get_password_hash(user_data.password1)
    await UserService.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login(response: Response, user_data: SUserAuth):
    user = await UserService.find_one_or_none(email=user_data.email)

    if not user or not verify_password(user_data.password1, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='These username and password is not valid')

    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)
    return {'access_token': access_token}
