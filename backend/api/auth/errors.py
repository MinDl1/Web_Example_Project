from typing import Dict, Union

from pydantic import BaseModel

from .ident.responses import IdentErrorCode


class ErrorModel(BaseModel):
    """
    Error model.

    @var detail: details of error
    """
    detail: Union[str, Dict[str, str]]


class ErrorCode(IdentErrorCode):
    """
    All Errors codes.
    """

    VALUE_ERROR = "VALUE_ERROR"
    ID_NOT_FOUND = "ID_NOT_FOUND"
    UNIQUE_ERROR = "UNIQUE_ERROR"
    FOREIGN_KEY_ERROR = "FOREIGN_KEY_ERROR"

    INVULNERABLE_ROLE = "INVULNERABLE_ROLE"
    ROLE_IS_USED_BY_USER = "ROLE_IS_USED_BY_USER"

    INVULNERABLE_USER = "INVULNERABLE_USER"
