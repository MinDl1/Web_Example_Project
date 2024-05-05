from asyncpg import Record
from pydantic import BaseModel
from typing import Optional


class RoleRead(BaseModel):
    id: int
    name: str


class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: Optional[str] = None
