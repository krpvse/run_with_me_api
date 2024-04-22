from fastapi import HTTPException, status


UserDoesNotExistsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='This user does not exists'
)

ExistingUserException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='User with this email already exists'
)

InvalidEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='These username and password is not valid'
)

TokenDoesNotExistsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Access token is not defined'
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='This access token is invalid'
)

ExpiredTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='This access token is expired'
)

NoPermissionsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='You have no permissions for this request'
)

NoParamException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Parameter you requested is not defined'
)
