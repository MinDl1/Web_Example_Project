from typing import Optional
from pydantic import BaseModel, Field


class Example(BaseModel):
    id: int
    test: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "test": "Example1",
                }
            ]
        }
    }


class ExampleCreate(BaseModel):
    test: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "test": "Example1",
                }
            ]
        }
    }


class ExampleUpdate(BaseModel):
    test: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "test": "Example1",
                }
            ]
        }
    }
