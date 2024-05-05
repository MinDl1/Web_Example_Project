from asyncpg import Record
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    role_id: int
    username: str
    hashed_password: str
    is_active: bool


class UserRead(BaseModel):
    id: int
    role_id: int
    role_name: str
    username: str
    is_active: bool


class UserReadMe(BaseModel):
    role_name: str
    username: str
    is_active: bool


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
