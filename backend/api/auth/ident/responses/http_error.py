from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Detail in HTTPException.

    Attributes:
        code: Error code.
        reason: Error reason.
    """
    code: str
    reason: str


class IdentErrorCode:
    """Аll authentication and authorization error codes.

    Attributes:
        BAD_CREDENTIALS: Bad credentials.
        USER_NOT_ACTIVE: User is not active.
        INVALID_TOKEN: Invalid token.
        ENDPOINT_NOT_FOUND: Endpoint not found.
        NO_ACCESS_RIGHTS: No required access rights.
        DATA_OUT_OF_DATE: The data is out of date.
    """
    BAD_CREDENTIALS = "BAD_CREDENTIALS"
    USER_NOT_ACTIVE = "USER_NOT_ACTIVE"
    INVALID_TOKEN = "INVALID_TOKEN"
    ENDPOINT_NOT_FOUND = "ENDPOINT_NOT_FOUND"
    NO_ACCESS_RIGHTS = "NO_ACCESS_RIGHTS"
    DATA_OUT_OF_DATE = "DATA_OUT_OF_DATE"


class HTTTPError:
    """Аll authentication and authorization errors.

    Attributes:
        BAD_CREDENTIALS_400: Bad credentials.
        BAD_CREDENTIALS_401: Could not validate credentials.
        INVALID_TOKEN_401: Invalid token.
        BAD_CREDENTIALS_403: Access token expires but refresh exists.
        NO_ACCESS_RIGHTS_403: No required access rights.
        USER_NOT_ACTIVE_403: User is not active.
        DATA_OUT_OF_DATE_403: User data is out of date, please re-login.
        ENDPOINT_NOT_FOUND_500: Endpoint not found.
    """
    BAD_CREDENTIALS_400 = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorDetail(
            code=IdentErrorCode.BAD_CREDENTIALS,
            reason="Bad credentials"
        ).model_dump(),
    )

    BAD_CREDENTIALS_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorDetail(
            code=IdentErrorCode.BAD_CREDENTIALS,
            reason="Could not validate credentials"
        ).model_dump(),
    )
    INVALID_TOKEN_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorDetail(
            code=IdentErrorCode.INVALID_TOKEN,
            reason="Invalid token"
        ).model_dump(),
    )

    BAD_CREDENTIALS_403 = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ErrorDetail(
            code=IdentErrorCode.BAD_CREDENTIALS,
            reason="Access token expires but refresh exists"
        ).model_dump(),
    )
    USER_NOT_ACTIVE_403 = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ErrorDetail(
            code=IdentErrorCode.USER_NOT_ACTIVE,
            reason="User is not active"
        ).model_dump(),
    )
    NO_ACCESS_RIGHTS_403 = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ErrorDetail(
            code=IdentErrorCode.NO_ACCESS_RIGHTS,
            reason="No required access rights"
        ).model_dump(),
    )
    DATA_OUT_OF_DATE_403 = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=ErrorDetail(
            code=IdentErrorCode.DATA_OUT_OF_DATE,
            reason="User data is out of date, please re-login"
        ).model_dump(),
    )

    ENDPOINT_NOT_FOUND_500 = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=ErrorDetail(
            code=IdentErrorCode.ENDPOINT_NOT_FOUND,
            reason="Endpoint not found"
        ).model_dump(),
    )
