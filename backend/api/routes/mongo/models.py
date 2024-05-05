import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    synopsis: str = Field(...)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                    "title": "Don Quixote",
                    "author": "Miguel de Cervantes",
                    "synopsis": "..."
                }
            ]
        }
    }


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    synopsis: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Don Quixote",
                    "author": "Miguel de Cervantes",
                    "synopsis": "..."
                }
            ]
        }
    }
