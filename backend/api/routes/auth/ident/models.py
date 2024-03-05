from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Union[int, None] = None
    role_id: Union[int, None] = None
    is_active: Union[bool, None] = None

    @classmethod
    def from_dict(cls, user_dict):
        return cls(**user_dict)
