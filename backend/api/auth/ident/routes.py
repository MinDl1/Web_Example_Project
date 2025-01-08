from fastapi import (
    APIRouter,
    Response,
    Request,
    status,
)

from ...postgresql import SessionDep

from .config import TokenName, SQLQueryParam, IdentUrl
from .jwt import Token
from .models import AccessToken, TokenData
from .utils import authenticate_user
from .sql_query import SQLQuery
from .responses import HTTTPError, IdentResponse
from .manager import OAuth2RequestFormDep
from .manager import CurrUserDep

router = APIRouter()
"""Ident router"""


@router.post(
    path=IdentUrl.LOGIN,
    summary="Authorization using OAuth2.0",
    description="Authorization in the application",
    response_description="Access token (Bearer) and refresh token (Cookie)",
    status_code=status.HTTP_200_OK,
    response_model=AccessToken,
    responses=IdentResponse.login_post,
)
async def login(
    form_data: OAuth2RequestFormDep,
    session: SessionDep,
    response: Response,
) -> AccessToken:
    """Login in system.

    Args:
        form_data: OAuth 2.0 form with login and passwd.
        session: Async db session.
        response: Endpoint response.

    Returns:
        Access token in body and refresh token in cookie response.

    Raises:
        HTTTPError.BAD_CREDENTIALS_400: If user with username in form not found.
    """
    user = (
        await session.execute(
            SQLQuery.user_one_username,
            {SQLQueryParam.username: form_data.username}
        )
    ).one_or_none()

    if not user:
        raise HTTTPError.BAD_CREDENTIALS_400

    token_data = authenticate_user(user, form_data.password)

    access_token = Token(TokenName.ACCESS_TOKEN, token_data=token_data).create_token()

    refresh_token = Token(TokenName.REFRESH_TOKEN, token_data=token_data).create_token()
    response.set_cookie(
        key=refresh_token.token_key,
        value=refresh_token.encoded_token,
        expires=refresh_token.expire_date,
        secure=refresh_token.secure,
        httponly=refresh_token.httponly,
    )

    return AccessToken(access_token=access_token.encoded_token, token_type=access_token.token_type)


@router.post(
    path=IdentUrl.REFRESH_TOKEN,
    summary="Refreshing access token",
    description="Refreshing access token with refresh token in Cookie",
    response_description="Bearer Token (Access)",
    status_code=status.HTTP_200_OK,
    response_model=AccessToken,
    responses=IdentResponse.refresh_access_token_post,
)
async def refresh_access_token(
    curr: CurrUserDep,
    session: SessionDep,
    request: Request,
) -> AccessToken:
    """Refresh access token by refresh token.

    Args:
        session: Async db session.
        request: Endpoint request.

    Returns:
        Access token in body response.

    Raises:
        raise HTTTPError.BAD_CREDENTIALS_401: If refresh token doesn't exist.
        raise HTTTPError.DATA_OUT_OF_DATE_403: If user data in database that stored in token data was modified.
    """
    refresh_token = Token(TokenName.REFRESH_TOKEN)
    refresh_token.encoded_token = request.cookies.get(refresh_token.token_key)
    if not refresh_token.encoded_token:
        raise HTTTPError.BAD_CREDENTIALS_401
    refresh_token.verify_token()

    user = (
        await session.execute(
            SQLQuery.user_one_id,
            {SQLQueryParam.id_user: refresh_token.token_data.sub}
        )
    ).one_or_none()
    if not user:
        raise HTTTPError.NO_ACCESS_RIGHTS_403

    if not user.is_active:
        raise HTTTPError.USER_NOT_ACTIVE_403

    token_data = TokenData.model_validate(user._asdict())
    if token_data != refresh_token.token_data:
        raise HTTTPError.DATA_OUT_OF_DATE_403

    access_token = Token(TokenName.ACCESS_TOKEN, token_data=token_data).create_token()

    return AccessToken(access_token=access_token.encoded_token, token_type=access_token.token_type)


@router.post(
    path=IdentUrl.LOGOUT,
    summary="Logout",
    description="Logout from application",
    response_description="Deleted refresh token (Cookie)",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=IdentResponse.logout_post,
)
async def logout(
    request: Request,
    response: Response,
) -> Response:
    """Logout.

    Args:
        request: Endpoint request.
        response: Endpoint response.

    Returns:
        HTTP status 204 no content.

    Raises:
        HTTTPError.BAD_CREDENTIALS_401: If refresh token doesn't exist.
    """
    refresh_token = Token(TokenName.REFRESH_TOKEN)
    refresh_token.encoded_token = request.cookies.get(refresh_token.token_key)
    if not refresh_token.encoded_token:
        raise HTTTPError.BAD_CREDENTIALS_401
    refresh_token.verify_token()

    response.delete_cookie(
        key=refresh_token.token_key,
        secure=refresh_token.secure,
        httponly=refresh_token.httponly,
    )

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
