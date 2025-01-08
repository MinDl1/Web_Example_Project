from routes.auth.config import (
    user_table_name,
    user_endpoint_table_name,
    role_table_name,
    endpoint_table_name,
    tag_table_name,
)


sql_user_me_select = f'''
    SELECT adu.username, 
        adr.name role_name, 
        adu.is_active
    FROM {user_table_name} adu
    JOIN {role_table_name} adr
    ON adr.id = 
        CASE 
            WHEN adu.id_extra_role is NULL THEN adu.id_base_role 
            WHEN NOW()::date BETWEEN adu.date_start_extra_role_id AND adu.date_stop_extra_role_id
                THEN adu.id_extra_role 
            ELSE adu.id_base_role 
        END
    WHERE adu.id = $1::INTEGER
        AND adu.is_deleted = False
        AND adr.is_deleted = False
'''

sql_user_select_one_user_id = f'''
    SELECT *
    FROM {user_table_name}
    WHERE id = $1::INTEGER
'''

sql_user_select_all = f'''
    SELECT adu.id, 
        adu.username, 
        adu.id_base_role,
        adu.id_extra_role,
        adu.date_start_extra_role_id,
        adu.date_stop_extra_role_id,
        adu.is_active
    FROM {user_table_name} adu
    WHERE adu.is_deleted = False
'''

sql_user_select_one_id = f'''
    SELECT adu.id, 
        adu.username, 
        adu.id_base_role,
        adu.id_extra_role,
        adu.date_start_extra_role_id,
        adu.date_stop_extra_role_id,
        adu.is_active
    FROM {user_table_name} adu
    WHERE adu.id = $1::INTEGER 
        AND adu.is_deleted = False
'''

sql_user_endpoints_select_one_id = f'''
    SELECT alue.id_endpoint, 
        alue.is_allow,
        adt.name tag_name, 
        adt.description tag_description, 
        ade.url, 
        ade.method, 
        ade.name,
        ade.description
    FROM {user_endpoint_table_name} alue
    JOIN {endpoint_table_name} ade
    ON ade.id = alue.id_endpoint
    JOIN {tag_table_name} adt
    ON adt.id = ade.id_tag
    WHERE alue.id_user = $1::INTEGER 
        AND alue.is_deleted = False
'''
