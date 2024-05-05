from typing import Annotated, List

from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    HTTPException,
    status,
    Body
)
import asyncpg.exceptions

from routes.auth.errors import ErrorCode
from routes.auth.ident.manager import (
    get_current_user,
    get_current_active_user,
    get_current_active_admin_user
)
from routes.auth.utils.sql_utils import update_record, delete_record
from routes.auth.config import user_table_name

from .models import User, UserRead, UserReadMe, UserUpdate
from .sql_querry import sql_user_select_one_id, sql_user_select_all
from .responses import (
    user_me_get_responses,
    user_me_patch_responses,
    user_me_delete_responses,
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
    current_user: Annotated[User, Depends(get_current_user)],
    request: Request
) -> UserReadMe:
    user = await request.app.postgresql.fetchrow(sql_user_select_one_id, current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"User with id {current_user.id} not found"
            },
        )

    return UserReadMe.model_validate(dict(user))


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
    user_update: UserUpdate = Body(...)
):
    id_not_found_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": ErrorCode.ID_NOT_FOUND,
            "reason": f"User with id {current_user.id} not found"
        },
    )

    sql_user_update_one, *values = update_record(
        model=user_update,
        table_name=user_table_name,
        record_id=current_user.id
    )
    try:
        user = await request.app.postgresql.fetchrow(sql_user_update_one, *values)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value error"
            },
        )
    if not user:
        raise id_not_found_exception

    user = await request.app.postgresql.fetchrow(sql_user_select_one_id, user["id"])
    if not user:
        raise id_not_found_exception

    return UserReadMe.model_validate(dict(user))


@router.delete(
    path="/me",
    summary="Delete the user info by id in access token",
    description="Delete the user info by id in access token",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=user_me_delete_responses,
)
async def delete_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request,
    response: Response
):
    sql_user_delete_one, value = delete_record(
        table_name=user_table_name,
        record_id=current_user.id
    )
    user = await request.app.postgresql.fetchrow(sql_user_delete_one, value)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"User with id {current_user.id} not found"
            },
        )

    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get(
    path="/all",
    summary="Shows list of all users",
    description="Shows list of all users",
    response_description="List of all users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserRead],
    responses=all_user_get_responses,
)
async def read_users_all(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
):
    users = await request.app.postgresql.fetch(sql_user_select_all)

    return [UserRead.model_validate(dict(row)) for row in users]


@router.get(
    path="/{id_u}",
    summary="Shows the user by id",
    description="Shows the user by id",
    response_description="The user",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    responses=user_get_responses,
)
async def read_user_by_id(
    id_u: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request
):
    user = await request.app.postgresql.fetchrow(sql_user_select_one_id, id_u)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"User with id {id_u} not found"
            },
        )

    return UserRead.model_validate(dict(user))


@router.patch(
    path="/{id_u}",
    summary="Update the user by id",
    description="Update the user by id",
    response_description="The user",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    responses=user_patch_responses,
)
async def update_user_by_id(
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
    try:
        user = await request.app.postgresql.fetchrow(sql_user_update_one, *values)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value error"
            },
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"User with id {id_u} not found"
            },
        )

    return UserRead.model_validate(dict(user))


@router.delete(
    path="/{id_u}",
    summary="Delete the user by id",
    description="Delete the user by id",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=user_delete_responses,
)
async def delete_user_by_id(
    id_u: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    request: Request,
    response: Response
):
    sql_user_delete_one, value = delete_record(
        table_name=user_table_name,
        record_id=id_u
    )
    user = await request.app.postgresql.fetchrow(sql_user_delete_one, value)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"User with id {id_u} not found"
            },
        )

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
