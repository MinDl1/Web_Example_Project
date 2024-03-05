from fastapi import APIRouter, Depends, Request, HTTPException, status, Body
from typing import Annotated, List

from .models import RoleRead, RoleUpdate, RoleCreate
from .sql_querry import sql_role_select_one_id, sql_role_select_all
from routes.auth.user.models import User
from routes.auth.ident.manager import get_current_active_admin_user
from routes.auth.utils.sql_utils import update_record, delete_record, insert_record
from routes.auth.config import role_table_name


router = APIRouter()


@router.post("/", response_model=RoleRead)
async def create_role(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request,
    role_create: RoleCreate = Body(...)
):
    sql_role_create_one, *values = insert_record(
        model=role_create,
        table_name=role_table_name
    )
    role = await request.app.postgresql.fetchrow(sql_role_create_one, *values)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this role in db"
            },
        )
    return RoleRead.from_dict(dict(role))


@router.get("/all", response_model=List[RoleRead])
async def read_roles(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
):
    roles = await request.app.postgresql.fetch(sql_role_select_all)

    if roles is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this role in db"
            },
        )

    return [RoleRead.from_dict(dict(row)) for row in roles]


@router.get("/{id_r}", response_model=RoleRead)
async def read_role(
    id_r: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
):
    role = await request.app.postgresql.fetchrow(sql_role_select_one_id, id_r)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this role in db"
            },
        )

    return RoleRead.from_dict(dict(role))


@router.patch("/{id_r}", response_model=RoleRead)
async def update_role(
    id_r: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request,
    role_update: RoleUpdate = Body(...)
):
    sql_role_update_one, *values = update_record(
        model=role_update,
        table_name=role_table_name,
        record_id=id_r
    )
    role = await request.app.postgresql.fetchrow(sql_role_update_one, *values)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this role in db"
            },
        )
    return RoleRead.from_dict(dict(role))


@router.delete("/{id_r}", response_model=RoleRead)
async def delete_role(
    id_r: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
):
    sql_role_delete_one, value = delete_record(
        table_name=role_table_name,
        record_id=id_r
    )
    print(sql_role_delete_one)
    role = await request.app.postgresql.fetchrow(sql_role_delete_one, value)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this role in db"
            },
        )

    return RoleRead.from_dict(dict(role))
