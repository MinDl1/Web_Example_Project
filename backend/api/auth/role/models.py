from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field

from ...auth.config import Table


class RoleBase(SQLModel):
    name: str
    description: str | None
    is_active: bool


class Role(RoleBase, table=True):

    __tablename__ = Table.role.name
    __table_args__ = {'schema': Table.role.schema}

    id: int | None = Field(default=None, primary_key=True)
    is_deleted: bool
    id_created_by: int
    created_date: datetime
    id_last_update_date: int | None
    last_update_date: datetime | None
    id_deleted_by: int | None
    deleted_date: datetime | None


class RoleRight(SQLModel, table=True):

    __tablename__ = Table.role_right.name
    __table_args__ = {'schema': Table.role_right.schema}

    id_role: int = Field(
        default=None,
        primary_key=True,
        foreign_key=Table.role.schema+'.'+Table.role.name+'.'+Table.default_id_name
    )
    id_endpoint: int = Field(
        default=None,
        primary_key=True,
        foreign_key=Table.endpoint.schema+'.'+Table.endpoint.name+'.'+Table.default_id_name
    )
    id_created_by: int
    created_date: datetime


"""class RoleEndpoint(BaseModel):
    id_endpoint: int
    tag_name: str
    tag_description: Optional[str] = None
    url: str
    method: str
    name: str
    description: Optional[str] = None


class RoleRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool


class RoleReadEndpoints(RoleRead):
    endpoints: Optional[list[RoleEndpoint]] = None


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool
    endpoints: Optional[list[int]] = None


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    endpoints: Optional[list[int]] = None


class RoleEndpointsCreate(BaseModel):
    id_role: int
    id_endpoint: int
    is_deleted: bool
    is_deleted_by: Optional[int] = None
    deleted_date: Optional[datetime] = None
"""