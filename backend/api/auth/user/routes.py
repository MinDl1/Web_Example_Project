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
    user_table_name,
    user_endpoint_table_name,
)
from routes.auth.ident.models import User
from routes.auth.ident.utils import verify_password
from routes.auth.ident.manager import get_current_active_user
from routes.auth.utils.sql_utils import update_record, delete_record, insert_record
from routes.auth.role.sql_query import sql_role_endpoints_select_one_id
from routes.auth.role.models import RoleEndpoint

from .models import (
    UserReadMe,
    UserUpdateMe,
    UserRead,
    UserUpdate,
    UserCreate,
    UserRight,
    UserEndpointsCreate,
    UserReadEndpoints,
)
from .sql_query import (
    sql_user_me_select,
    sql_user_select_one_id,
    sql_user_select_one_user_id,
    sql_user_select_all,
    sql_user_endpoints_select_one_id,
)
from .responses import (
    user_me_get_responses,
    user_me_patch_responses,
    create_user_post_responses,
    all_user_get_responses,
    user_get_responses,
    user_patch_responses,
    user_delete_responses,
)


router = APIRouter()


@router.get(
    path="/me",
    summary="Shows the user info by id in access token",
    description="Shows the user info by id in access token",
    response_description="User info",
    status_code=status.HTTP_200_OK,
    response_model=UserReadMe,
    responses=user_me_get_responses,
)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request
) -> UserReadMe:
    async with request.app.postgresql.acquire() as postgres_conn:
        user = await postgres_conn.fetchrow(sql_user_me_select, current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"User with id {current_user.id} not found"
            },
            headers={"response-error": "ID_NOT_FOUND"},
        )
    user = UserReadMe.model_validate(dict(user))

    async with request.app.postgresql.acquire() as postgres_conn:
        user_endpoints = await postgres_conn.fetch(sql_user_endpoints_select_one_id, current_user.id)
    if user_endpoints:
        user_endpoints = [UserEndpoint.model_validate(dict(row)) for row in user_endpoints]
        user.endpoints_user = user_endpoints

    async with request.app.postgresql.acquire() as postgres_conn:
        role_endpoints = await postgres_conn.fetch(sql_role_endpoints_select_one_id, current_user.id_role)
    if user_endpoints:
        role_endpoints = [RoleEndpoint.model_validate(dict(row)) for row in role_endpoints]
        user.endpoints_role = role_endpoints

    return user


@router.patch(
    path="/me",
    summary="Update the user info by id in access token",
    description="Update the user info by id in access token",
    response_description="User info",
    status_code=status.HTTP_200_OK,
    response_model=UserReadMe,
    responses=user_me_patch_responses,
)
async def update_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    user_update: UserUpdateMe = Body(...)
) -> UserReadMe:
    id_not_found_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": ErrorCode.ID_NOT_FOUND,
            "reason": f"User with id {current_user.id} not found"
        },
        headers={"response-error": "ID_NOT_FOUND"},
    )

    async with request.app.postgresql.acquire() as postgres_conn:
        user = await postgres_conn.fetchrow(sql_user_select_one_user_id, current_user.id)

    if not verify_password(user_update.old_password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.BAD_CREDENTIALS,
                "reason": f"BAD_CREDENTIALS"
            },
            headers={"response-error": "BAD_CREDENTIALS"},
        )

    user_update_dict = user_update.model_dump(exclude={'old_password'}, exclude_none=True)

    sql_user_update_one, *values = update_record(
        model=user_update_dict,
        table_name=user_table_name,
        record_id=current_user.id,
        id_last_update_by=current_user.id
    )
    try:
        async with request.app.postgresql.acquire() as postgres_conn:
            user = await postgres_conn.fetchrow(sql_user_update_one, *values)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value error"
            },
            headers={"response-error": "UNIQUE_ERROR"},
        )
    if not user:
        raise id_not_found_exception

    async with request.app.postgresql.acquire() as postgres_conn:
        user = await postgres_conn.fetchrow(sql_user_me_select, current_user.id)
    if not user:
        raise id_not_found_exception
    user = UserReadMe.model_validate(dict(user))

    async with request.app.postgresql.acquire() as postgres_conn:
        user_endpoints = await postgres_conn.fetch(sql_user_endpoints_select_one_id, current_user.id)
    if user_endpoints:
        user_endpoints = [UserEndpoint.model_validate(dict(row)) for row in user_endpoints]
        user.endpoints_user = user_endpoints

    async with request.app.postgresql.acquire() as postgres_conn:
        role_endpoints = await postgres_conn.fetch(sql_role_endpoints_select_one_id, current_user.id_role)
    if user_endpoints:
        role_endpoints = [RoleEndpoint.model_validate(dict(row)) for row in role_endpoints]
        user.endpoints_role = role_endpoints

    return user


@router.post(
    path="/",
    summary="Create a new user",
    description="Create a new user",
    response_description="The created user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
    responses=create_user_post_responses,
)
async def create_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    user_create: UserCreate = Body(...)
) -> UserRead:
    if user_create.endpoints:
        id_user_update_endpoints = [endpoint.id_endpoint for endpoint in user_create.endpoints]
        if len(user_create.endpoints) != len(set(id_user_update_endpoints)):
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
            user_create_dict = user_create.model_dump(exclude={'endpoints'}, exclude_none=True)
            sql_user_create_one, *values = insert_record(
                model=user_create_dict,
                table_name=user_table_name,
                id_created_by=current_user.id
            )
            try:
                user = await postgres_conn.fetchrow(sql_user_create_one, *values)
            except asyncpg.exceptions.UniqueViolationError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "code": ErrorCode.UNIQUE_ERROR,
                        "reason": "Unique value error"
                    },
                    headers={"response-error": "UNIQUE_ERROR"},
                )
            except asyncpg.exceptions.ForeignKeyViolationError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "code": ErrorCode.FOREIGN_KEY_ERROR,
                        "reason": "Foreign key error in Role"
                    },
                    headers={"response-error": "FOREIGN_KEY_ERROR"},
                )
            user = UserRead.model_validate(dict(user))

            if user_create.endpoints:
                user_sql_endpoints_model = None
                user_endpoints_list = []
                for endpoint in user_create.endpoints:
                    if user.is_active:
                        user_endpoint_row = UserEndpointsCreate(
                            id_user=user.id,
                            id_endpoint=endpoint.id_endpoint,
                            is_allow=endpoint.is_allow,
                            is_deleted=not user.is_active
                        )
                        user_sql_endpoints_model = user_endpoint_row
                    else:
                        user_endpoint_row = UserEndpointsCreate(
                            id_user=user.id,
                            id_endpoint=endpoint.id_endpoint,
                            is_allow=endpoint.is_allow,
                            is_deleted=user.is_active,
                            id_deleted_by=current_user.id,
                            deleted_date=datetime.datetime.now()
                        )
                        user_sql_endpoints_model = user_endpoint_row

                    user_endpoints_list.append(tuple(user_endpoint_row.model_dump(exclude_none=True).values()))

                sql_user_endpoints_create, *values = insert_record(
                    model=user_sql_endpoints_model,
                    table_name=user_endpoint_table_name,
                    id_created_by=current_user.id
                )
                try:
                    await postgres_conn.executemany(sql_user_endpoints_create, user_endpoints_list)
                except asyncpg.exceptions.ForeignKeyViolationError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": ErrorCode.FOREIGN_KEY_ERROR,
                            "reason": "Foreign key error in Endpoints"
                        },
                        headers={"response-error": "FOREIGN_KEY_ERROR"},
                    )

    return user


@router.get(
    path="/all",
    summary="Shows list of all users",
    description="Shows list of all users",
    response_description="List of all users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserRead],
    responses=all_user_get_responses,
)
async def read_users(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request
) -> List[UserRead]:
    async with request.app.postgresql.acquire() as postgres_conn:
        users = await postgres_conn.fetch(sql_user_select_all)

    return [UserRead.model_validate(dict(row)) for row in users]


@router.get(
    path="/{id_u}",
    summary="Shows the user by id",
    description="Shows the user by id",
    response_description="The user",
    status_code=status.HTTP_200_OK,
    response_model=UserReadEndpoints,
    responses=user_get_responses,
)
async def read_user(
    id_u: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request
) -> UserReadEndpoints:
    async with request.app.postgresql.acquire() as postgres_conn:
        user = await postgres_conn.fetchrow(sql_user_select_one_id, id_u)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"User with id {id_u} not found"
            },
            headers={"response-error": "ID_NOT_FOUND"},
        )
    user = UserReadEndpoints.model_validate(dict(user))

    async with request.app.postgresql.acquire() as postgres_conn:
        user_endpoints = await postgres_conn.fetch(sql_user_endpoints_select_one_id, id_u)
    if user_endpoints:
        user_endpoints = [UserEndpoint.model_validate(dict(row)) for row in user_endpoints]
        user.endpoints = user_endpoints

    return user


@router.patch(
    path="/{id_u}",
    summary="Update the user by id",
    description="Update the user by id",
    response_description="The user",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    responses=user_patch_responses,
)
async def update_user(
    id_u: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    user_update: UserUpdate = Body(...)
) -> UserRead:
    if id_u == 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.INVULNERABLE_USER,
                "reason": f"User with id {id_u} is invulnerable"
            },
            headers={"response-error": "INVULNERABLE_USER"},
        )

    if user_update.endpoints:
        id_user_update_endpoints = [endpoint.id_endpoint for endpoint in user_update.endpoints]
        if len(user_update.endpoints) != len(set(id_user_update_endpoints)):
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
            "reason": f"User with id {id_u} not found"
        },
        headers={"response-error": "ID_NOT_FOUND"},
    )

    user_endpoints_update = user_update.endpoints

    async with request.app.postgresql.acquire() as postgres_conn:
        user = await postgres_conn.fetchrow(sql_user_select_one_id, id_u)
    if not user:
        raise id_not_found_error
    user = UserRead.model_validate(dict(user))

    async with request.app.postgresql.acquire() as postgres_conn:
        async with postgres_conn.transaction():
            user_update_dict = user_update.model_dump(exclude={'endpoints'}, exclude_none=True)
            if user_update_dict:
                sql_user_update_one, *values = update_record(
                    model=user_update_dict,
                    table_name=user_table_name,
                    record_id=id_u,
                    id_last_update_by=current_user.id
                )
                try:
                    user = await postgres_conn.fetchrow(sql_user_update_one, *values)
                except asyncpg.exceptions.UniqueViolationError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": ErrorCode.UNIQUE_ERROR,
                            "reason": "Unique value error"
                        },
                        headers={"response-error": "UNIQUE_ERROR"},
                    )
                except asyncpg.exceptions.ForeignKeyViolationError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": ErrorCode.FOREIGN_KEY_ERROR,
                            "reason": "Foreign key error"
                        },
                        headers={"response-error": "FOREIGN_KEY_ERROR"},
                    )
                if not user:
                    raise id_not_found_error
                user = UserRead.model_validate(dict(user))

            if user_endpoints_update:
                sql_user_endpoints_delete, *values = delete_record(
                    table_name=user_endpoint_table_name,
                    record_id=id_u,
                    id_field_name="id_user",
                    id_deleted_by=current_user.id
                )
                await postgres_conn.fetchrow(sql_user_endpoints_delete, *values)

                user_sql_endpoints_model = None
                user_endpoints_list = []
                for endpoint in user_endpoints_update:
                    if user.is_active:
                        user_endpoint_row = UserEndpointsCreate(
                            id_user=id_u,
                            id_endpoint=endpoint.id_endpoint,
                            is_allow=endpoint.is_allow,
                            is_deleted=not user.is_active
                        )
                        user_sql_endpoints_model = user_endpoint_row
                    else:
                        user_endpoint_row = UserEndpointsCreate(
                            id_user=id_u,
                            id_endpoint=endpoint.id_endpoint,
                            is_allow=endpoint.is_allow,
                            is_deleted=user.is_active,
                            id_deleted_by=current_user.id,
                            deleted_date=datetime.datetime.now()
                        )
                        user_sql_endpoints_model = user_endpoint_row

                    user_endpoints_list.append(tuple(user_endpoint_row.model_dump(exclude_none=True).values()))

                sql_user_endpoints_create, *values = insert_record(
                    model=user_sql_endpoints_model,
                    table_name=user_endpoint_table_name,
                    id_created_by=current_user.id
                )

                try:
                    await postgres_conn.executemany(sql_user_endpoints_create, user_endpoints_list)
                except asyncpg.exceptions.ForeignKeyViolationError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": ErrorCode.FOREIGN_KEY_ERROR,
                            "reason": "Foreign key error"
                        },
                        headers={"response-error": "FOREIGN_KEY_ERROR"},
                    )

            if not user_update_dict and not user_endpoints_update:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "code": ErrorCode.VALUE_ERROR,
                        "reason": "No fields to update"
                    },
                    headers={"response-error": "VALUE_ERROR"},
                )

    return user


@router.delete(
    path="/{id_u}",
    summary="Delete the user by id",
    description="Delete the user by id",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=user_delete_responses,
)
async def delete_user(
    id_u: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    response: Response
) -> Response:
    if id_u == 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.INVULNERABLE_USER,
                "reason": f"User with id {id_u} is invulnerable"
            },
            headers={"response-error": "INVULNERABLE_USER"},
        )

    id_not_found_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": ErrorCode.ID_NOT_FOUND,
            "reason": f"User with id {id_u} not found"
        },
        headers={"response-error": "ID_NOT_FOUND"},
    )

    async with request.app.postgresql.acquire() as postgres_conn:
        user = await postgres_conn.fetchrow(sql_user_select_one_id, id_u)
    if not user:
        raise id_not_found_error

    sql_user_delete_one, *values = delete_record(
        table_name=user_table_name,
        record_id=id_u,
        id_deleted_by=current_user.id
    )
    async with request.app.postgresql.acquire() as postgres_conn:
        user = await postgres_conn.fetchrow(sql_user_delete_one, *values)
    if not user:
        raise id_not_found_error

    sql_user_endpoints_delete, *values = delete_record(
        table_name=user_endpoint_table_name,
        record_id=id_u,
        id_field_name="id_user",
        id_deleted_by=current_user.id
    )
    async with request.app.postgresql.acquire() as postgres_conn:
        await postgres_conn.fetchrow(sql_user_endpoints_delete, *values)

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
