from fastapi import APIRouter, Request

from .utils import create_user_query
from routes.auth.user.models import UserRead, UserCreate


router = APIRouter()


@router.post("/register")
async def register_user(
    request: Request,
    user_create: UserCreate
):
    sql_user_create_one, *values = create_user_query(user_create)
    created_user = await request.app.postgresql.fetchrow(sql_user_create_one, *values)
    return UserRead.from_dict(created_user)
