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
    ID_NOT_FOUND = "ID_NOT_FOUND"
    UNIQUE_ERROR = "UNIQUE_ERROR"
