from typing import List

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
import asyncpg.exceptions

from routes.auth.utils.sql_utils import update_record, delete_record, insert_record

from .models import Example, ExampleCreate, ExampleUpdate
from .sql_querry import (
    sql_example_select,
    sql_example_select_one
)
from routes.auth.errors import ErrorCode
from .responses import (
    postgres_post_responses,
    postgres_get_responses,
    postgres_get_one_delete_responses,
    postgres_patch_responses,
)


router = APIRouter()


@router.post(
    path="/",
    summary="Create a new example",
    description="Create a new example",
    response_description="The created example",
    status_code=status.HTTP_201_CREATED,
    response_model=Example,
    responses=postgres_post_responses,
)
async def create_example(request: Request, example_create: ExampleCreate = Body(...)) -> Example:
    sql_create_example, *values = insert_record(example_create, "example1")
    try:
        example = await request.app.postgresql.fetchrow(sql_create_example, *values)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value error"
            },
        )

    if not example:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Example1 with ID {example_create.test} not found"
            },
        )

    return Example.model_validate(dict(example))


@router.get(
    path="/",
    summary="Shows list of all examples",
    description="Shows list of all examples",
    response_description="List of all examples",
    status_code=status.HTTP_200_OK,
    response_model=List[Example],
    responses=postgres_get_responses,
)
async def list_example(request: Request) -> List[Example]:
    example = await request.app.postgresql.fetch(sql_example_select)

    return [Example.model_validate(dict(row)) for row in example]


@router.get(
    path="/{id_p}",
    summary="Shows the example by id",
    description="Shows the example by id",
    response_description="The single example",
    status_code=status.HTTP_200_OK,
    response_model=Example,
    responses=postgres_get_one_delete_responses,
)
async def find_example(id_p: int, request: Request) -> Example:
    example = await request.app.postgresql.fetchrow(sql_example_select_one, id_p)
    if not example:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Example1 with ID {id_p} not found"
            },
        )

    return Example.model_validate(dict(example))


@router.patch(
    path="/{id_p}",
    summary="Update the example by id",
    description="Update the example by id",
    response_description="The single example",
    status_code=status.HTTP_200_OK,
    response_model=Example,
    responses=postgres_patch_responses
)
async def update_example(
    id_p: int,
    request: Request,
    example_update: ExampleUpdate = Body(...)
) -> Example:
    sql_example_update_one, *values = update_record(
        model=example_update,
        table_name='example1',
        record_id=id_p
    )
    try:
        example = await request.app.postgresql.fetchrow(sql_example_update_one, *values)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value error"
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

    return Example.model_validate(dict(example))


@router.delete(
    path="/{id_p}",
    summary="Delete the example by id",
    description="Delete the example by id",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=postgres_get_one_delete_responses
)
async def delete_example(
    id_p: int,
    request: Request,
    response: Response
) -> Response:
    sql_example_delete_one, value = delete_record(
        table_name='example1',
        record_id=id_p
    )
    example = await request.app.postgresql.fetchrow(sql_example_delete_one, value)
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
