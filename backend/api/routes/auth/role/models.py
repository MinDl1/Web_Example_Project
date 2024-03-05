from pydantic import BaseModel
from typing import Optional


class RoleRead(BaseModel):
    id: int
    name: str

    @classmethod
    def from_dict(cls, user_dict):
        return cls(**user_dict)


class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: Optional[str] = None
