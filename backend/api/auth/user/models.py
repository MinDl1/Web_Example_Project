from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field
from pydantic import BaseModel

from ...auth.config import Table

from ..role.models import RoleRight


class UserBase(SQLModel):
    username: str
    id_base_role: int = Field(
        default=None,
        foreign_key=Table.role.schema+'.'+Table.role.name+'.'+Table.default_id_name
    )
    id_extra_role: int | None = Field(
        default=None,
        foreign_key=Table.role.schema+'.'+Table.role.name+'.'+Table.default_id_name
    )
    date_start_extra_role: datetime | None
    date_stop_extra_role: datetime | None
    is_active: bool


class User(UserBase, table=True):

    __tablename__ = Table.user.name
    __table_args__ = {'schema': Table.user.schema}

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_deleted: bool
    id_created_by: int | None
    created_date: datetime
    id_last_update_by: int | None
    last_update_date: datetime | None
    id_deleted_by: int | None
    deleted_date: datetime | None


class UserRight(SQLModel, table=True):

    __tablename__ = Table.user_right.name
    __table_args__ = {'schema': Table.user_right.schema}

    id_user: int = Field(
        default=None,
        primary_key=True,
        foreign_key=Table.user.schema+'.'+Table.user.name+'.'+Table.default_id_name
    )
    id_endpoint: int = Field(
        default=None,
        primary_key=True,
        foreign_key=Table.endpoint.schema+'.'+Table.endpoint.name+'.'+Table.default_id_name
    )
    is_allow: bool
    id_created_by: int
    created_date: datetime


"""class UserEndpoint(BaseModel):
    id_endpoint: int
    is_allow: bool
    tag_name: str
    tag_description: Optional[str] = None
    url: str
    method: str
    name: str
    description: Optional[str] = None


class UserReadMe(BaseModel):
    username: str
    role_name: str
    is_active: bool
    endpoints_user: Optional[list[UserEndpoint]] = None
    endpoints_role: Optional[list[RoleEndpoint]] = None


class UserUpdateMe(BaseModel):
    old_password: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    id_base_role: int
    id_extra_role: Optional[int] = None
    date_start_extra_role_id: Optional[datetime] = None
    date_stop_extra_role_id: Optional[datetime] = None
    is_active: bool


class UserReadEndpoints(UserRead):
    endpoints: Optional[list[UserEndpoint]] = None


class EndpointAllow(BaseModel):
    id_endpoint: int
    is_allow: bool


class UserCreate(BaseModel):
    username: str
    password: str
    id_base_role: int
    id_extra_role: Optional[int] = None
    date_start_extra_role_id: Optional[datetime] = None
    date_stop_extra_role_id: Optional[datetime] = None
    is_active: bool
    endpoints: Optional[list[EndpointAllow]] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    id_base_role: Optional[int] = None
    id_extra_role: Optional[int] = None
    date_start_extra_role_id: Optional[datetime] = None
    date_stop_extra_role_id: Optional[datetime] = None
    is_active: Optional[bool] = None
    endpoints: Optional[list[EndpointAllow]] = None


class UserEndpointsCreate(BaseModel):
    id_user: int
    id_endpoint: int
    is_allow: bool
    is_deleted: bool
    is_deleted_by: Optional[int] = None
    deleted_date: Optional[datetime] = None
"""