class TableSpec:
    def __init__(self, schema: str, name: str):
        self.schema = schema
        self.name = name


class Table:
    default_id_name = 'id'

    role = TableSpec('auth', 'role')
    role_right = TableSpec('auth', 'role_right')

    user = TableSpec('auth', 'user')
    user_right = TableSpec('auth', 'user_right')

    endpoint = TableSpec('auth', 'endpoint')
    tag = TableSpec('auth', 'tag')
