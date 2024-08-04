from routes.auth.config import user_table_name, role_table_name


sql_user_select_one_id = f'''
    SELECT {user_table_name}.id, {user_table_name}.role_id, {user_table_name}.username, {user_table_name}.email,
        {user_table_name}.hashed_password, {user_table_name}.is_active, {role_table_name}.name as role_name
    FROM {user_table_name}
    JOIN {role_table_name}
    ON {user_table_name}.role_id = {role_table_name}.id
    WHERE {user_table_name}.id = $1::INTEGER
'''

sql_user_select_all = f'''
    SELECT {user_table_name}.id, {user_table_name}.role_id, {user_table_name}.username, {user_table_name}.email,
        {user_table_name}.hashed_password, {user_table_name}.is_active, {role_table_name}.name as role_name
    FROM {user_table_name}
    JOIN {role_table_name}
    ON {user_table_name}.role_id = {role_table_name}.id
'''
