from routes.auth.config import user_table_name


sql_user_select_one_username = f'''
    SELECT D$User.id, D$User.role_id, D$User.username, D$User.hashed_password, D$User.is_active
    FROM {user_table_name}
    WHERE D$User.username = $1::VARCHAR
'''

sql_user_select_one_id = f'''
    SELECT D$User.id, D$User.role_id, D$User.username, D$User.hashed_password, D$User.is_active
    FROM {user_table_name}
    WHERE D$User.id = $1::INTEGER
'''
