from routes.auth.config import role_table_name


sql_role_select_one_id = f'''
    SELECT {role_table_name}.id, {role_table_name}.name
    FROM {role_table_name}
    WHERE {role_table_name}.id = $1::INTEGER
'''

sql_role_select_all = f'''
    SELECT {role_table_name}.id, {role_table_name}.name
    FROM {role_table_name}
'''
