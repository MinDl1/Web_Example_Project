from typing import Annotated

import asyncpg.exceptions
from fastapi import (
    APIRouter,
    Request,
    Depends,
    status,
    HTTPException,
)

from routes.auth.errors import ErrorCode
from routes.auth.user.models import UserCreate, UserReadMe
from routes.auth.ident.manager import get_current_active_admin_user_or_false
from routes.auth.ident.models import TokenData
from routes.auth.user.sql_querry import sql_user_select_one_id

from .utils import create_user_query
from .responses import register_user_post_responses


router = APIRouter()


@router.post(
    path="/register",
    summary="Authorization using OAuth2.0",
    description="Authorization in the application",
    response_description="Access token (Bearer) and refresh token (Cookie)",
    status_code=status.HTTP_201_CREATED,
    response_model=UserReadMe,
    responses=register_user_post_responses,
)
async def register_user(
    current_user: Annotated[TokenData, Depends(get_current_active_admin_user_or_false)],
    request: Request,
    user_create: UserCreate
) -> UserReadMe:
    sql_user_create_one, *values = create_user_query(user_create, current_user)
    try:
        created_user = await request.app.postgresql.fetchrow(sql_user_create_one, *values)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UNIQUE_ERROR,
                "reason": "Unique value error"
            },
        )

    created_user = await request.app.postgresql.fetchrow(sql_user_select_one_id, created_user["id"])
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.ID_NOT_FOUND,
                "reason": f"User with username {user_create.username} not found"
            },
        )

    return UserReadMe.model_validate(dict(created_user))
