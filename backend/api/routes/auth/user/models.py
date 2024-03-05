from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    role_id: int
    username: str
    hashed_password: str
    is_active: bool

    @classmethod
    def from_dict(cls, user_dict):
        return cls(**user_dict)


class UserRead(BaseModel):
    role_id: int
    username: str
    is_active: bool

    @classmethod
    def from_dict(cls, user_dict):
        return cls(**user_dict)


class UserReadMe(BaseModel):
    role_name: str
    username: str
    is_active: bool

    @classmethod
    def from_dict(cls, user_dict):
        return cls(**user_dict)


class UserCreate(BaseModel):
    role_id: int
    username: str
    password: str
    is_active: bool


class UserUpdate(BaseModel):
    role_id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
