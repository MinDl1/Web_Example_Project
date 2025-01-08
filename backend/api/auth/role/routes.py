import datetime

from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    HTTPException,
    status,
    Body,
)
from typing import Annotated, List
import asyncpg.exceptions

from routes.auth.errors import ErrorCode
from routes.auth.config import (
    role_table_name,
    role_endpoint_table_name,
)
from routes.auth.ident.models import User
from routes.auth.ident.manager import get_current_active_user
from routes.auth.utils.sql_utils import update_record, delete_record, insert_record

from .models import (
    RoleRead,
    RoleUpdate,
    RoleCreate,
    RoleEndpoint,
    RoleEndpointsCreate,
    RoleReadEndpoints,
)
from .sql_query import (
    sql_role_select_one_id,
    sql_role_select_all,
    sql_role_endpoints_select_one_id,
    sql_user_select_role,
)
from .responses import (
    create_role_post_responses,
    all_role_get_responses,
    role_get_responses,
    role_patch_responses,
    role_delete_responses,
)


router = APIRouter()


@router.post(
    path="/",
    summary="Create a new role",
    description="Create a new role",
    response_description="The created role",
    status_code=status.HTTP_201_CREATED,
    response_model=RoleRead,
    responses=create_role_post_responses,
)
async def create_role(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    role_create: RoleCreate = Body(...)
) -> RoleRead:
    if role_create.endpoints:
        if len(role_create.endpoints) != len(set(role_create.endpoints)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.UNIQUE_ERROR,
                    "reason": "Unique value error"
                },
                headers={"response-error": "UNIQUE_ERROR"},
            )

    async with request.app.postgresql.acquire() as postgres_conn:
        async with postgres_conn.transaction():
            role_create_dict = role_create.model_dump(exclude={'endpoints'}, exclude_none=True)
            sql_role_create_one, *values = insert_record(
                model=role_create_dict,
                table_name=role_table_name,
                id_created_by=current_user.id
            )
            try:
                role = await postgres_conn.fetchrow(sql_role_create_one, *values)
            except asyncpg.exceptions.UniqueViolationError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "code": ErrorCode.UNIQUE_ERROR,
                        "reason": "Unique value error"
                    },
                    headers={"response-error": "UNIQUE_ERROR"},
                )
            role = RoleRead.model_validate(dict(role))

            if role_create.endpoints:
                role_sql_endpoints_model = None
                role_endpoints_list = []
                for id_endpoint in role_create.endpoints:
                    if role.is_active:
                        role_endpoint_row = RoleEndpointsCreate(
                            id_role=role.id,
                            id_endpoint=id_endpoint,
                            is_deleted=not role.is_active
                        )
                        role_sql_endpoints_model = role_endpoint_row
                    else:
                        role_endpoint_row = RoleEndpointsCreate(
                            id_role=role.id,
                            id_endpoint=id_endpoint,
                            is_deleted=role.is_active,
                            id_deleted_by=current_user.id,
                            deleted_date=datetime.datetime.now()
                        )
                        role_sql_endpoints_model = role_endpoint_row

                    role_endpoints_list.append(tuple(role_endpoint_row.model_dump(exclude_none=True).values()))

                sql_role_endpoints_create, *values = insert_record(
                    model=role_sql_endpoints_model,
                    table_name=role_endpoint_table_name,
                    id_created_by=current_user.id
                )
                try:
                    await postgres_conn.executemany(sql_role_endpoints_create, role_endpoints_list)
                except asyncpg.exceptions.ForeignKeyViolationError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": ErrorCode.FOREIGN_KEY_ERROR,
                            "reason": "Foreign key error"
                        },
                        headers={"response-error": "FOREIGN_KEY_ERROR"},
                    )

        return role


@router.get(
    path="/all",
    summary="Shows list of all roles",
    description="Shows list of all roles",
    response_description="List of all roles",
    status_code=status.HTTP_200_OK,
    response_model=List[RoleRead],
    responses=all_role_get_responses,
)
async def read_roles(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request
) -> List[RoleRead]:
    async with request.app.postgresql.acquire() as postgres_conn:
        roles = await postgres_conn.fetch(sql_role_select_all)

    return [RoleRead.model_validate(dict(row)) for row in roles]


@router.get(
    path="/{id_r}",
    summary="Shows the role by id",
    description="Shows the role by id",
    response_description="The role",
    status_code=status.HTTP_200_OK,
    response_model=RoleReadEndpoints,
    responses=role_get_responses,
)
async def read_role(
    id_r: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request
) -> RoleReadEndpoints:
    async with request.app.postgresql.acquire() as postgres_conn:
        role = await postgres_conn.fetchrow(sql_role_select_one_id, id_r)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Role with id {id_r} not found"
            },
            headers={"response-error": "ID_NOT_FOUND"},
        )
    role = RoleReadEndpoints.model_validate(dict(role))

    async with request.app.postgresql.acquire() as postgres_conn:
        role_endpoints = await postgres_conn.fetch(sql_role_endpoints_select_one_id, id_r)
    if role_endpoints:
        role_endpoints = [RoleEndpoint.model_validate(dict(row)) for row in role_endpoints]
        role.endpoints = role_endpoints

    return role


@router.patch(
    path="/{id_r}",
    summary="Update the role by id",
    description="Update the role by id",
    response_description="The role",
    status_code=status.HTTP_200_OK,
    response_model=RoleRead,
    responses=role_patch_responses,
)
async def update_role(
    id_r: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    role_update: RoleUpdate = Body(...)
) -> RoleRead:
    if id_r == 1 or id_r == 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.INVULNERABLE_ROLE,
                "reason": f"Role with id {id_r} is invulnerable"
            },
            headers={"response-error": "INVULNERABLE_ROLE"},
        )

    if role_update.endpoints:
        if len(role_update.endpoints) != len(set(role_update.endpoints)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.UNIQUE_ERROR,
                    "reason": "Unique value error"
                },
                headers={"response-error": "UNIQUE_ERROR"},
            )

    id_not_found_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": ErrorCode.ID_NOT_FOUND,
            "reason": f"Role with id {id_r} not found"
        },
        headers={"response-error": "ID_NOT_FOUND"},
    )

    role_endpoints_update = role_update.endpoints

    async with request.app.postgresql.acquire() as postgres_conn:
        role = await postgres_conn.fetchrow(sql_role_select_one_id, id_r)
    if not role:
        raise id_not_found_error
    role = RoleRead.model_validate(dict(role))

    async with request.app.postgresql.acquire() as postgres_conn:
        async with postgres_conn.transaction():
            role_update_dict = role_update.model_dump(exclude={'endpoints'}, exclude_none=True)
            if role_update_dict:
                sql_role_update_one, *values = update_record(
                    model=role_update_dict,
                    table_name=role_table_name,
                    record_id=id_r,
                    id_last_update_by=current_user.id
                )
                try:
                    role = await postgres_conn.fetchrow(sql_role_update_one, *values)
                except asyncpg.exceptions.UniqueViolationError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": ErrorCode.UNIQUE_ERROR,
                            "reason": "Unique value error"
                        },
                        headers={"response-error": "UNIQUE_ERROR"},
                    )
                if not role:
                    raise id_not_found_error
                role = RoleRead.model_validate(dict(role))

            if role_endpoints_update:
                sql_role_endpoints_delete, *values = delete_record(
                    table_name=role_endpoint_table_name,
                    record_id=id_r,
                    id_field_name="id_role",
                    id_deleted_by=current_user.id
                )
                await postgres_conn.fetchrow(sql_role_endpoints_delete, *values)

                role_sql_endpoints_model = None
                role_endpoints_list = []
                for id_endpoint in role_endpoints_update:
                    if role.is_active:
                        role_endpoint_row = RoleEndpointsCreate(
                            id_role=id_r,
                            id_endpoint=id_endpoint,
                            is_deleted=not role.is_active
                        )
                        role_sql_endpoints_model = role_endpoint_row
                    else:
                        role_endpoint_row = RoleEndpointsCreate(
                            id_role=id_r,
                            id_endpoint=id_endpoint,
                            is_deleted=role.is_active,
                            id_deleted_by=current_user.id,
                            deleted_date=datetime.datetime.now()
                        )
                        role_sql_endpoints_model = role_endpoint_row

                    role_endpoints_list.append(tuple(role_endpoint_row.model_dump(exclude_none=True).values()))

                sql_role_endpoints_create, *values = insert_record(
                    model=role_sql_endpoints_model,
                    table_name=role_endpoint_table_name,
                    id_created_by=current_user.id
                )

                try:
                    await postgres_conn.executemany(sql_role_endpoints_create, role_endpoints_list)
                except asyncpg.exceptions.ForeignKeyViolationError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": ErrorCode.FOREIGN_KEY_ERROR,
                            "reason": "Foreign key error"
                        },
                        headers={"response-error": "FOREIGN_KEY_ERROR"},
                    )

            if not role_update_dict and not role_endpoints_update:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "code": ErrorCode.VALUE_ERROR,
                        "reason": "No fields to update"
                    },
                    headers={"response-error": "VALUE_ERROR"},
                )

    return role


@router.delete(
    path="/{id_r}",
    summary="Delete the role by id",
    description="Delete the role by id",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=role_delete_responses,
)
async def delete_role(
    id_r: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    response: Response
) -> Response:
    if id_r == 1 or id_r == 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.INVULNERABLE_ROLE,
                "reason": f"Role with id {id_r} is invulnerable"
            },
            headers={"response-error": "INVULNERABLE_ROLE"},
        )

    id_not_found_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": ErrorCode.ID_NOT_FOUND,
            "reason": f"Role with id {id_r} not found"
        },
        headers={"response-error": "ID_NOT_FOUND"},
    )

    async with request.app.postgresql.acquire() as postgres_conn:
        role = await postgres_conn.fetchrow(sql_role_select_one_id, id_r)
    if not role:
        raise id_not_found_error

    async with request.app.postgresql.acquire() as postgres_conn:
        user_with_role = await postgres_conn.fetchrow(sql_user_select_role, id_r)
    if user_with_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ROLE_IS_USED_BY_USER,
                "reason": f"Role with id {id_r} is used by user"
            },
            headers={"response-error": "ROLE_IS_USED_BY_USER"},
        )

    sql_role_delete_one, *values = delete_record(
        table_name=role_table_name,
        record_id=id_r,
        id_deleted_by=current_user.id
    )
    async with request.app.postgresql.acquire() as postgres_conn:
        role = await postgres_conn.fetchrow(sql_role_delete_one, *values)
    if not role:
        raise id_not_found_error

    sql_role_endpoints_delete, *values = delete_record(
        table_name=role_endpoint_table_name,
        record_id=id_r,
        id_field_name="id_role",
        id_deleted_by=current_user.id
    )
    async with request.app.postgresql.acquire() as postgres_conn:
        await postgres_conn.fetchrow(sql_role_endpoints_delete, *values)

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
