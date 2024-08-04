from routes.auth.config import user_table_name


sql_id_select_one_email = f'''
    SELECT email
    FROM {user_table_name}
    WHERE email = $1::VARCHAR
'''
