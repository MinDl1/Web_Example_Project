from routes.auth.config import user_table_name


sql_user_select_one_username = f'''
    SELECT id, role_id, username, hashed_password, is_active
    FROM {user_table_name}
    WHERE username = $1::VARCHAR
'''

sql_user_select_one_id = f'''
    SELECT id, role_id, username, hashed_password, is_active
    FROM {user_table_name}
    WHERE id = $1::INTEGER
'''
