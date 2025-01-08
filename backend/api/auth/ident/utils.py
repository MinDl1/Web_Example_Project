from typing import Any

from sqlalchemy import Row

from ..utils.passwd_hash import pwd_context

from .responses import HTTTPError
from .models import TokenData


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies password.

    Verifies password with hashed password.

    Args:
        plain_password: Password to check.
        hashed_password: Hashed password.

    Returns:
        A bool, if password success verified True, else False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: Row[Any], password: str) -> TokenData:
    """Authenticates user.

    Authenticates user by password and active flag.

    Args:
        user: User data.
        password: Password to check.

    Returns:
        User token data.

    Raises:
        HTTTPError.BAD_CREDENTIALS_400: If password unsuccessfully verified.
        HTTTPError.USER_IS_NOT_ACTIVE_403: If user is not active.
    """
    if not verify_password(password, user.hashed_password):
        raise HTTTPError.BAD_CREDENTIALS_400
    if not user.is_active:
        raise HTTTPError.USER_NOT_ACTIVE_403
    return TokenData.model_validate(user._asdict())
