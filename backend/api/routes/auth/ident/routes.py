from typing import Annotated

from fastapi import Depends
from fastapi import (
    APIRouter,
    Response,
    Request,
    HTTPException,
    status,
    # Cookie,
)
from fastapi.security import OAuth2PasswordRequestForm

from routes.auth.errors import ErrorCode

from .jwt import create_access_token, create_refresh_token, verify_token
from .manager import get_current_user
from .models import Token, TokenData
from .utils import authenticate_user
from .sql_querry import sql_user_select_one_username
from .responses import (
    token_post_responses,
    refresh_access_token_post_responses,
    logout_post_responses,
)


router = APIRouter()


@router.post(
    path="/token",
    summary="Authorization using OAuth2.0",
    description="Authorization in the application",
    response_description="Access token (Bearer) and refresh token (Cookie)",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses=token_post_responses,
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    response: Response,
) -> Token:
    user = await request.app.postgresql.fetchrow(sql_user_select_one_username, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.LOGIN_BAD_CREDENTIALS,
                "reason": "LOGIN_BAD_CREDENTIALS"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = authenticate_user(dict(user), form_data.password)
    access_token = create_access_token(
        data={"id": user.id, "role_id": user.role_id, "is_active": user.is_active}
    )
    create_refresh_token(
        data={"id": user.id, "role_id": user.role_id, "is_active": user.is_active},
        response=response
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    path="/refresh_access_token",
    summary="Refreshing access token",
    description="Refreshing access token with refresh token in Cookie",
    response_description="Bearer Token (Access)",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses=refresh_access_token_post_responses,
)
async def refresh_access_token(
    request: Request,
    # refresh_token: Annotated[str | None, Cookie()] = None
) -> Token:
    refresh_token = request.cookies.get('refresh_token')
    user = await verify_token(refresh_token, request)
    access_token = create_access_token(
        data={"id": user.id, "role_id": user.role_id, "is_active": user.is_active}
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    path="/logout",
    summary="Logout",
    description="Logout from application",
    response_description="Deleted refresh token (Cookie)",
    status_code=status.HTTP_200_OK,
    responses=logout_post_responses,
)
async def logout_user(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    response: Response
) -> Response:
    response.delete_cookie(
        key="refresh_token",
        secure=False,
        httponly=True,
    )
    response.status_code = status.HTTP_200_OK
    return response
