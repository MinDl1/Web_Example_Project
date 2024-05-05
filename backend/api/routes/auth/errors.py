from enum import Enum
from typing import Dict, Union

from pydantic import BaseModel


class ErrorModel(BaseModel):
    """
    Error model.

    @var detail: details of error
    """
    detail: Union[str, Dict[str, str]]


class ErrorCode(str, Enum):
    """
    All Errors codes.
    """
    LOGIN_BAD_CREDENTIALS = "LOGIN_BAD_CREDENTIALS"
    LOGIN_USER_IS_NOT_ACTIVE = "LOGIN_USER_IS_NOT_ACTIVE"
    INVALID_TOKEN = "INVALID_TOKEN"
    BAD_CREDENTIALS = "BAD_CREDENTIALS"
    NOT_ADMIN_USER = "NOT_ADMIN_USER"
    UNIQUE_ERROR = "UNIQUE_ERROR"
    ID_NOT_FOUND = "ID_NOT_FOUND"
    VALUE_ERROR = "VALUE_ERROR"
