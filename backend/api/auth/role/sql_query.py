from routes.auth.config import (
    user_table_name,
    role_table_name,
    role_endpoint_table_name,
    endpoint_table_name,
    tag_table_name,
)


sql_role_select_all = f'''
    SELECT adr.id, 
        adr.name, 
        adr.description, 
        adr.is_active
    FROM {role_table_name} adr
    WHERE adr.is_deleted = False
'''

sql_role_select_one_id = f'''
    SELECT adr.id, 
        adr.name, 
        adr.description, 
        adr.is_active
    FROM {role_table_name} adr
    WHERE adr.id = $1::INTEGER 
        AND adr.is_deleted = False
'''

sql_role_endpoints_select_one_id = f'''
    SELECT alre.id_endpoint, 
        adt.name tag_name, 
        adt.description tag_description, 
        ade.url, 
        ade.method, 
        ade.name,
        ade.description
    FROM {role_endpoint_table_name} alre
    JOIN {endpoint_table_name} ade
    ON ade.id = alre.id_endpoint
    JOIN {tag_table_name} adt
    ON adt.id = ade.id_tag
    WHERE alre.id_role = $1::INTEGER 
        AND alre.is_deleted = False
'''

sql_user_select_role = f'''
    SELECT adu.id
    FROM {user_table_name} adu
    WHERE (adu.id_base_role = $1::INTEGER OR adu.id_extra_role = $1::INTEGER) 
        AND adu.is_deleted = False
'''
