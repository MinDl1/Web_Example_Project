from fastapi import APIRouter, Depends, Request, HTTPException, status, Body
from typing import Annotated, List

from .models import User, UserRead, UserReadMe, UserUpdate
from .sql_querry import sql_user_select_one_id, sql_user_select_all
from routes.auth.ident.manager import get_current_user, get_current_active_user, get_current_active_admin_user
from routes.auth.utils.sql_utils import update_record, delete_record
from routes.auth.config import user_table_name


router = APIRouter()


@router.get("/me", response_model=UserReadMe)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
    request: Request
) -> UserReadMe:
    user = await request.app.postgresql.fetchrow(sql_user_select_one_id, current_user.id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this user in db"
            },
        )

    return UserReadMe.from_dict(dict(user))


@router.patch("/me", response_model=UserRead)
async def update_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    user_update: UserUpdate = Body(...)
):
    sql_user_update_one, *values = update_record(
        model=user_update,
        table_name=user_table_name,
        record_id=current_user.id
    )
    user = await request.app.postgresql.fetchrow(sql_user_update_one, *values)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this user in db"
            },
        )
    return UserRead.from_dict(dict(user))


@router.delete("/me", response_model=UserRead)
async def update_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request
):
    sql_user_delete_one, value = delete_record(
        table_name=user_table_name,
        record_id=current_user.id
    )
    user = await request.app.postgresql.fetchrow(sql_user_delete_one, value)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this user in db"
            },
        )

    return UserRead.from_dict(dict(user))


@router.get("/all", response_model=List[UserReadMe])
async def read_users(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
):
    users = await request.app.postgresql.fetch(sql_user_select_all)

    if users is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this user in db"
            },
        )

    return [UserReadMe.from_dict(dict(row)) for row in users]


@router.get("/{id_u}", response_model=UserReadMe)
async def read_users(
    id_u: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
):
    user = await request.app.postgresql.fetchrow(sql_user_select_one_id, id_u)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this user in db"
            },
        )

    return UserReadMe.from_dict(dict(user))


@router.patch("/{id_u}", response_model=UserRead)
async def update_user(
    id_u: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request,
    user_update: UserUpdate = Body(...)
):
    sql_user_update_one, *values = update_record(
        model=user_update,
        table_name=user_table_name,
        record_id=id_u
    )
    user = await request.app.postgresql.fetchrow(sql_user_update_one, *values)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this user in db"
            },
        )
    return UserRead.from_dict(dict(user))


@router.delete("/{id_u}", response_model=UserRead)
async def update_user(
    id_u: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
):
    sql_user_delete_one, value = delete_record(
        table_name=user_table_name,
        record_id=id_u
    )
    user = await request.app.postgresql.fetchrow(sql_user_delete_one, value)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ID_NOT_FOUND",
                "reason": f"No this user in db"
            },
        )

    return UserRead.from_dict(dict(user))
