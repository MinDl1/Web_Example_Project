from pydantic import BaseModel
from typing import Optional

from sqlmodel import SQLModel, Field

from ...auth.config import Table


class Endpoint(SQLModel, table=True):

    __tablename__ = Table.endpoint.name
    __table_args__ = {'schema': Table.endpoint.schema}

    id: int | None = Field(default=None, primary_key=True)
    id_tag: int
    url: str
    method: str
    name: str
    description: str | None


"""class Endpoint(BaseModel):
    id: int
    tag_name: str
    tag_description: Optional[str] = None
    url: str
    method: str
    name: str
    description: Optional[str] = None"""
