from datetime import datetime
from typing import Optional
from ipaddress import IPv4Address, IPv6Address

from sqlalchemy import MetaData
from sqlmodel import SQLModel, Field


class LogsAPIBase(SQLModel):
    id_user: Optional[int] = Field(default=None)
    client_host: str
    client_port: int
    url: str
    method: str
    query_params: Optional[str]
    path_params: Optional[str]
    response_code: Optional[int]
    response_error: Optional[str]
    api_date_time: datetime
    execution_time: Optional[float]


class LogsAPI(LogsAPIBase, table=True):

    __tablename__ = "api"
    __table_args__ = {'schema': 'logs'}

    id: int = Field(default=None, primary_key=True)
    write_date_time: datetime = Field(default_factory=datetime.now)


class LogsAPICreate(LogsAPIBase):
    id_user: Optional[int] = None
    client_host: str
    client_port: int
    url: str
    method: str
    query_params: Optional[str] = None
    path_params: Optional[str] = None
    response_code: Optional[int] = None
    response_error: Optional[str] = None
    api_date_time: datetime = None
    execution_time: Optional[float] = None
