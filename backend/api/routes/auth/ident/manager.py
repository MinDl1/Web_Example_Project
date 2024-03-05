from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request, Cookie

from .jwt import verify_token, verify_access_token
from routes.auth.user.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


async def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)],
                           request: Request,
                           refresh_token: Annotated[str | None, Cookie()] = None) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = False
    if access_token is not None:
        user = await verify_access_token(access_token, request)
    if not user and refresh_token:
        await verify_token(refresh_token, request)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access token expires but refresh exists"
        )
    elif user and refresh_token:
        return user
    else:
        raise credentials_exception


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_admin_user(
    current_active_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    if current_active_user.role_id != 1:
        raise HTTPException(status_code=400, detail="Not admin user")
    return current_active_user
