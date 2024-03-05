from fastapi import APIRouter, Body, Request, Response, HTTPException, status
import asyncpg.exceptions

from .models import Example, ExampleCreate, ExampleUpdate
from .sql_querry import (
    sql_example_select,
    sql_example_select_one,
    sql_example_create,
    sql_example_update,
    sql_example_delete,
)
from .errors import ErrorCode
from .responses import (
    postgres_post_responses,
    postgres_get_responses,
    postgres_get_one_delete_responses,
    postgres_patch_responses,
)


router = APIRouter()


@router.post("/", summary="Create a new example", description="Create a new example",
             response_description="The created example", status_code=status.HTTP_201_CREATED,
             response_model=Example, responses=postgres_post_responses)
async def create_example(request: Request, example_create: ExampleCreate = Body(...)):
    try:
        example = await request.app.postgresql.fetchrow(sql_example_create, example_create.test)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value"
            },
        )
    return dict(example)


@router.get("/", summary="Shows list of all examples", description="Shows list of all examples",
            response_description="List of all examples", status_code=status.HTTP_200_OK,
            response_model=list[Example], responses=postgres_get_responses)
async def list_example(request: Request):
    example = await request.app.postgresql.fetch(sql_example_select)
    return [dict(row) for row in example]


@router.get("/{id_p}", summary="Shows the example by id", description="Shows the example by id",
            response_description="The single example", status_code=status.HTTP_200_OK,
            response_model=Example, responses=postgres_get_one_delete_responses)
async def find_example(id_p: int, request: Request):
    example = await request.app.postgresql.fetchrow(sql_example_select_one, id_p)
    if not example:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Example1 with ID {id_p} not found"
            },
        )
    return dict(example)


@router.patch("/{id_p}", summary="Update the example by id", description="Update the example by id",
              response_description="The single example", status_code=status.HTTP_200_OK,
              response_model=Example, responses=postgres_patch_responses)
async def update_example(id_p: int, request: Request, example_update: ExampleUpdate = Body(...)):
    try:
        example = await request.app.postgresql.fetchrow(sql_example_update, example_update.test, id_p)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value"
            },
        )
    if not example:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Example1 with ID {id_p} not found"
            },
        )
    return dict(example)


@router.delete("/{id_p}", summary="Delete the example by id", description="Delete the example by id",
               response_description="HTTP 200 STATUS", responses=postgres_get_one_delete_responses)
async def delete_example(id_p: int, request: Request, response: Response):
    example = await request.app.postgresql.fetchrow(sql_example_delete, id_p)
    if not example:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Example1 with ID {id_p} not found"
            },
        )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
