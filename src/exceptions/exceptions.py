from fastapi import HTTPException, status


UserDoesNotExistException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='This user does not exist'
)

NotExistingConfirmationCodeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='This confirmation code does not exist'
)

NotConfirmedEmailException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Email is not confirmed. Check out link in email'
)

ExistingUserException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
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
    detail='Token is invalid'
)

ExpiredTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token is expired'
)

FailedToCreateTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Failed to create token'
)

NoPermissionsException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='You have no permissions for this request'
)

NoParamException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Parameter you requested is not defined'
)

UnknownAPIException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Something went wrong'
)
