from datetime import datetime, timedelta, timezone
from enum import Enum

from jose import jwt, JWTError
from pydantic import ValidationError

from ...config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
    REFRESH_SECRET_KEY,
    ALGORITHM,
)

from .config import issuer, SQLQueryParam
from .responses import HTTTPError
from .models import TokenData


class TokenSpec(Enum):
    """A JWT token specification.

    Attributes:
        ACCESS_TOKEN: Access token.
        REFRESH_TOKEN: Refresh token.

        token_key: Token key name.
        token_type: Token type.
        exp_minutes: Expire time in minutes.
        secret_key: Secret key for JWT.
        algorithm: JWT algorithm.
        auto_error: Raise auto error while checking.
        secure: Secure for cookie.
        httponly: HTTP only for cookie.
    """
    ACCESS_TOKEN = (
        'access_token',
        'Bearer',
        ACCESS_TOKEN_EXPIRE_MINUTES,
        ACCESS_SECRET_KEY,
        ALGORITHM,
        False
    )
    REFRESH_TOKEN = (
        'refresh_token',
        'Cookie',
        REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60,
        REFRESH_SECRET_KEY,
        ALGORITHM,
        True,
        False,
        True
    )

    def __init__(
        self,
        token_key: str,
        token_type: str,
        exp_minutes: int,
        secret_key: str,
        algorithm: str,
        auto_error: bool,
        secure: bool = None,
        httponly: bool = None
    ):
        """Initializes the instance based on token specifications.

        Args:
            token_key: Token key name.
            token_type: Token type.
            exp_minutes: Expire time in minutes.
            secret_key: Secret key for JWT.
            algorithm: JWT algorithm.
            auto_error: Raise auto error while checking.
            secure: Secure for cookie.
            httponly: HTTP only for cookie.
        """
        self.token_key = token_key
        self.token_type = token_type
        self.exp_minutes = exp_minutes
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.auto_error = auto_error
        self.secure = secure
        self.httponly = httponly


class Token:
    """Token specification, data, encoded JWT etc.

    Attributes:
        token_key: Token key name.
        token_type: Token type.
        exp_minutes: Expire time in minutes.
        secret_key: Secret key for JWT.
        algorithm: JWT algorithm.
        auto_error: Raise auto error while checking.
        secure: Secure for cookie.
        httponly: HTTP only for cookie.
        expire_date: Expire token date time.
        encoded_token: Encoded JWT.
        token_data: Token data.
    """

    def __init__(
        self,
        token_name: str,
        encoded_token: str = None,
        token_data: TokenData = None
    ):
        """Initializes the instance based on token specifications, encoded token and token data.

        Args:
            token_name: Token name from TokenSpec.
            encoded_token: Encoded JWT.
            token_data: Token data.
        """
        token_spec = TokenSpec[token_name]
        self.token_key = token_spec.token_key
        self.token_type = token_spec.token_type
        self.exp_minutes = token_spec.exp_minutes
        self.secret_key = token_spec.secret_key
        self.algorithm = token_spec.algorithm
        self.auto_error = token_spec.auto_error
        self.secure = token_spec.secure
        self.httponly = token_spec.httponly
        self.expire_date = None
        self.encoded_token = encoded_token
        self.token_data = token_data

    def create_token(self) -> 'Token':
        """Creates encoded JWT.

        Creates encoded JWT from token data and specification.

        Returns:
            The instance with expire_date and encoded_token.
        """
        to_encode = self.token_data.model_dump()
        to_encode.update({SQLQueryParam.id_user: str(to_encode.get(SQLQueryParam.id_user))})
        iat_date = datetime.now(timezone.utc)
        expire_date = iat_date + timedelta(minutes=self.exp_minutes)
        to_encode.update({"iss": issuer, "exp": expire_date, "iat": iat_date})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        self.expire_date = expire_date
        self.encoded_token = encoded_jwt

        return self

    def verify_token(self) -> 'Token':
        """Verifies encoded JWT.

        Verifies encoded JWT from encoded token and token specification.

        Returns:
            The instance with token data.

        Raises:
            HTTTPError.INVALID_TOKEN_401: If token specification auto error and JWT decode fails.
        """
        if self.encoded_token is None:
            if self.auto_error:
                raise HTTTPError.INVALID_TOKEN_401
            return self
        try:
            payload = jwt.decode(self.encoded_token, self.secret_key, algorithms=[self.algorithm])
            try:
                token_data = TokenData.model_validate(payload)
            except ValidationError:
                if self.auto_error:
                    raise HTTTPError.INVALID_TOKEN_401
                return self

            self.token_data = token_data
            return self
        except JWTError:
            if self.auto_error:
                raise HTTTPError.INVALID_TOKEN_401
            return self
