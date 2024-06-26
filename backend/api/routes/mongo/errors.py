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
    ID_EXISTS_ERROR = "ID_EXISTS_ERROR"
    DATA_NOT_MODIFIED = "DATA_NOT_MODIFIED"
