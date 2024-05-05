from asyncpg import Record
from fastapi import HTTPException, status

from routes.auth.errors import ErrorCode
from routes.auth.utils.passwd_hash import pwd_context

from .models import TokenData


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: dict, password: str) -> TokenData:
    if not verify_password(password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.LOGIN_BAD_CREDENTIALS,
                "reason": "LOGIN_BAD_CREDENTIALS"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.LOGIN_USER_IS_NOT_ACTIVE,
                "reason": "LOGIN_USER_IS_NOT_ACTIVE"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenData.model_validate(user)
