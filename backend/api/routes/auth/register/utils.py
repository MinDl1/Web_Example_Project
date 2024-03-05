from routes.auth.utils.sql_utils import insert_record
from routes.auth.ident.utils import pwd_context


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user_query(user_create):
    user_create_dict = dict(user_create)
    hashed_password = get_password_hash(user_create_dict["password"])
    user_create_dict.pop("password")
    user_create_dict.update({"hashed_password": hashed_password})

    sql_query, *values = insert_record(user_create_dict, "D$User")

    return sql_query, *values
