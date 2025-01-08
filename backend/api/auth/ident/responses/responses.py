from fastapi import status

from .http_error import HTTTPError
from .utils import convert_to_example


base_auth_responses = {
    status.HTTP_401_UNAUTHORIZED: convert_to_example([
        HTTTPError.BAD_CREDENTIALS_401,
        HTTTPError.INVALID_TOKEN_401,
    ]),
    status.HTTP_403_FORBIDDEN: convert_to_example([
        HTTTPError.BAD_CREDENTIALS_403,
        HTTTPError.NO_ACCESS_RIGHTS_403,
        HTTTPError.USER_NOT_ACTIVE_403,
        HTTTPError.DATA_OUT_OF_DATE_403,
    ]),
    status.HTTP_500_INTERNAL_SERVER_ERROR: convert_to_example([
        HTTTPError.ENDPOINT_NOT_FOUND_500,
    ]),
}
"""Base authorization responses."""


class IdentResponse:
    """Ident responses.

    Attributes:
        login_post: Responses for login
        refresh_access_token_post: Responses for refresh token
        logout_post: Responses for logout
    """
    login_post = {
        status.HTTP_400_BAD_REQUEST: convert_to_example([
            HTTTPError.BAD_CREDENTIALS_400,
        ]),
        status.HTTP_403_FORBIDDEN: convert_to_example([
            HTTTPError.USER_NOT_ACTIVE_403,
        ]),
    }
    refresh_access_token_post = {
        status.HTTP_401_UNAUTHORIZED: convert_to_example([
            HTTTPError.BAD_CREDENTIALS_401,
            HTTTPError.INVALID_TOKEN_401,
        ]),
        status.HTTP_403_FORBIDDEN: convert_to_example([
            HTTTPError.NO_ACCESS_RIGHTS_403,
            HTTTPError.USER_NOT_ACTIVE_403,
            HTTTPError.DATA_OUT_OF_DATE_403,
        ]),
    }
    logout_post = {
        status.HTTP_401_UNAUTHORIZED: convert_to_example([
            HTTTPError.BAD_CREDENTIALS_401,
            HTTTPError.INVALID_TOKEN_401,
        ]),
    }
