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
from routes.auth.user.models import User
from routes.auth.ident.manager import get_current_active_admin_user
from routes.auth.utils.sql_utils import update_record, delete_record, insert_record
from routes.auth.config import role_table_name

from .models import RoleRead, RoleUpdate, RoleCreate
from .sql_querry import sql_role_select_one_id, sql_role_select_all
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
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request,
    role_create: RoleCreate = Body(...)
) -> RoleRead:
    sql_role_create_one, *values = insert_record(
        model=role_create,
        table_name=role_table_name
    )
    try:
        role = await request.app.postgresql.fetchrow(sql_role_create_one, *values)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value error"
            },
        )
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Role with name {role_create.name} not found"
            },
        )

    return RoleRead.model_validate(dict(role))


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
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
) -> List[RoleRead]:
    roles = await request.app.postgresql.fetch(sql_role_select_all)

    return [RoleRead.model_validate(dict(row)) for row in roles]


@router.get(
    path="/{id_r}",
    summary="Shows the role by id",
    description="Shows the role by id",
    response_description="The role",
    status_code=status.HTTP_200_OK,
    response_model=RoleRead,
    responses=role_get_responses,
)
async def read_role(
    id_r: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
) -> RoleRead:
    role = await request.app.postgresql.fetchrow(sql_role_select_one_id, id_r)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Role with id {id_r} not found"
            },
        )

    return RoleRead.model_validate(dict(role))


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
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request,
    role_update: RoleUpdate = Body(...)
) -> RoleRead:
    sql_role_update_one, *values = update_record(
        model=role_update,
        table_name=role_table_name,
        record_id=id_r
    )
    try:
        role = await request.app.postgresql.fetchrow(sql_role_update_one, *values)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value error"
            },
        )
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Role with id {id_r} not found"
            },
        )

    return RoleRead.model_validate(dict(role))


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
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request,
    response: Response
) -> Response:
    sql_role_delete_one, value = delete_record(
        table_name=role_table_name,
        record_id=id_r
    )
    role = await request.app.postgresql.fetchrow(sql_role_delete_one, value)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"Role with id {id_r} not found"
            },
        )

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
