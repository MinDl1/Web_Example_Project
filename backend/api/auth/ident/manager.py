from typing import Annotated
import re

from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession

from ...postgresql import SessionDep

from .config import TokenName, SQLQueryParam, IdentUrl, IDENT_TAG

from .jwt import Token
from .sql_query import SQLQuery
from .models import TokenData
from .responses import HTTTPError


OAuth2BearerDep = Annotated[str | None, Depends(
    OAuth2PasswordBearer(tokenUrl=IDENT_TAG+IdentUrl.LOGIN, auto_error=False)
)]
"""Dependence for user authorization, get Bearer token."""
OAuth2RequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
"""Dependence for login, request form."""


async def fetch_endpoint(
    url_path: str,
    method: str,
    session: AsyncSession,
) -> int:
    """Fetches ID endpoint by url and method from Database.

    Args:
        url_path: Endpoint URL.
        method: Endpoint method.
        session: Async db session.

    Returns:
        ID endpoint.

    Raises:
        HTTTPError.ENDPOINT_NOT_FOUND_500: If no endpoint was found.
    """
    url = re.sub(r'\d+', '', url_path)
    endpoint = (
        await session.execute(
            SQLQuery.endpoint_one, {
                SQLQueryParam.url: url,
                SQLQueryParam.method: method
            }
        )
    ).one_or_none()

    if not endpoint:
        raise HTTTPError.ENDPOINT_NOT_FOUND_500

    return endpoint.id


async def check_access(
    token: Token,
    id_endpoint: int,
    session: AsyncSession,
) -> TokenData | None:
    """Checks User access for endpoint.

    Args:
        token: Token with data.
        id_endpoint: Endpoint ID.
        session: Async db session.

    Returns:
        The token data if user has access.
        None if user hasn`t access and token auto error is off.

    Raises:
        HTTTPError.NO_ACCESS_RIGHTS_403: If token auto error is on and no token data or user hasn`t access
        or no token data or no user in database.
        HTTTPError.DATA_OUT_OF_DATE_403: If user data in database that stored in token data was modified.
    """
    if not token.token_data:
        if token.auto_error:
            raise HTTTPError.NO_ACCESS_RIGHTS_403
        return None

    user = (
        await session.execute(
            SQLQuery.user_one_right,
            {
                **token.token_data.model_dump(include={SQLQueryParam.id_user}),
                **{SQLQueryParam.id_endpoint: id_endpoint}
            }
        )
    ).one_or_none()
    if user:
        if not user.is_allow:
            if token.auto_error:
                raise HTTTPError.NO_ACCESS_RIGHTS_403
            return None
    else:
        user = (
            await session.execute(
                SQLQuery.user_one_role_right,
                {
                    **token.token_data.model_dump(include={SQLQueryParam.id_user}),
                    **{SQLQueryParam.id_endpoint: id_endpoint}
                }
            )
        ).one_or_none()

    if not user:
        if token.auto_error:
            raise HTTTPError.NO_ACCESS_RIGHTS_403
        return None

    if not user.is_active:
        raise HTTTPError.USER_NOT_ACTIVE_403

    token_data = TokenData.model_validate(user._asdict())
    if token_data != token.token_data:
        if token.auto_error:
            raise HTTTPError.DATA_OUT_OF_DATE_403
        return None

    return token_data


async def auth_current_user(
    access_encoded_token: OAuth2BearerDep,
    request: Request,
    session: SessionDep,
) -> TokenData:
    """Authorization user by access and refresh token.

    Args:
        access_encoded_token: Encoded access token.
        request: User request.
        session: Async db session.

    Returns:
        The user token data.

    Raises:
        HTTTPError.BAD_CREDENTIALS_403: If rights check for the access token failed,
        but refresh token passed successfully.
        HTTTPError.BAD_CREDENTIALS_401: If access and refresh tokens don't exist.
    """
    id_endpoint = await fetch_endpoint(request.url.path, request.method, session)

    refresh_token = Token(TokenName.REFRESH_TOKEN)
    refresh_token.encoded_token = request.cookies.get(refresh_token.token_key)
    access_token = Token(TokenName.ACCESS_TOKEN, encoded_token=access_encoded_token)
    user = None
    if access_token.encoded_token and refresh_token.encoded_token:
        access_token.verify_token()
        user = await check_access(access_token, id_endpoint, session)
    if refresh_token.encoded_token:
        refresh_token.verify_token()
        if not user:
            await check_access(refresh_token, id_endpoint, session)
            raise HTTTPError.BAD_CREDENTIALS_403
        return user
    raise HTTTPError.BAD_CREDENTIALS_401


CurrUserDep = Annotated[TokenData, Depends(auth_current_user)]
"""Dependence for user authorization by access and refresh token."""


async def auth_current_user_or_none(
    access_encoded_token: OAuth2BearerDep,
    request: Request,
    session: SessionDep,
) -> TokenData:
    """Authorization user by access and refresh token or None.

    Args:
        access_encoded_token: Encoded access token.
        request: User request.
        session: Async db session.

    Returns:
        The user token data if user has access or None.

    Raises:
        All raises from auth_current_user.
    """
    try:
        current_user = await auth_current_user(access_encoded_token, request, session)
    except HTTPException as e:
        if e.status_code == HTTTPError.BAD_CREDENTIALS_401.status_code:
            current_user = None
        else:
            raise e
    return current_user


CurrUserNoneDep = Annotated[TokenData, Depends(auth_current_user_or_none)]
"""Dependence for user authorization by access and refresh token or None."""
