from typing import Any

from routes.auth.ident.models import TokenData
from routes.auth.user.models import UserCreate
from routes.auth.utils.sql_utils import insert_record


def create_user_query(user_create: UserCreate, current_user: TokenData) -> tuple[str, Any]:
    user_create_dict = dict(user_create)

    if not current_user:
        user_create_dict.update({"role_id": 2})
        user_create_dict.update({"is_active": True})

    sql_query, *values = insert_record(user_create_dict, "D$User")

    return sql_query, *values
