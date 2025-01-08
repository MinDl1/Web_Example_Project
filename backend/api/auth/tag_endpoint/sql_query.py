from routes.auth.config import (
    endpoint_table_name,
    tag_table_name,
)


sql_endpoints_select_all = f'''
    SELECT ade.id, 
        adt.name tag_name, 
        adt.description tag_description, 
        ade.url, 
        ade.method, 
        ade.name,
        ade.description
    FROM {endpoint_table_name} ade
    JOIN {tag_table_name} adt
    ON adt.id = ade.id_tag
'''
