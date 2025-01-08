from pydantic import BaseModel, field_validator, field_serializer

from .config import SQLQueryParam


class AccessToken(BaseModel):
    """An Access token that returns to user.

    Attributes:
        access_token: Encoded jwt token with TokenData.
        token_type: Token type (Bearer).
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """A token JWT data.

    Connected with .sql_query.py.

    Attributes:
        sub: ID user.
        roles: User active role ID.
    """
    sub: int
    roles: int
    # groups: int

    @field_validator(SQLQueryParam.id_user, mode="before")
    def convert_sub_to_int(cls, value: str):
        """Try to convert sub to int before validation.

        Args:
            value: Sub value.

        Returns:
            Sub value.
        """
        try:
            return int(value)
        except ValueError:
            return value
