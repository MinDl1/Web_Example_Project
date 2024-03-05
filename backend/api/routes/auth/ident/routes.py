from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter, Response, Request, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from .jwt import create_access_token, create_refresh_token, verify_token
from .manager import get_current_user
from .models import Token, TokenData
from .utils import authenticate_user
from .sql_querry import sql_user_select_one_username


router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    response: Response,
) -> Token:
    user = await request.app.postgresql.fetchrow(sql_user_select_one_username, form_data.username)
    if user is not None:
        user = authenticate_user(dict(user), form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"id": user.id, "role_id": user.role_id, "is_active": user.is_active}
    )
    create_refresh_token(
        data={"id": user.id, "role_id": user.role_id, "is_active": user.is_active},
        response=response
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/refresh_access_token")
async def refresh_access_token(
    request: Request,
    refresh_token: Annotated[str | None, Cookie()] = None
) -> Token:
    user = await verify_token(refresh_token, request)
    access_token = create_access_token(
        data={"id": user.id, "role_id": user.role_id, "is_active": user.is_active}
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def logout_user(current_user: Annotated[TokenData, Depends(get_current_user)], response: Response):
    response.delete_cookie(
        key="refresh_token",
        secure=False,
        httponly=True,
    )
    response.status_code = status.HTTP_200_OK
    return response
