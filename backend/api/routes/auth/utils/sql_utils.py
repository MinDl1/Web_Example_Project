import datetime
from typing import Optional
from pydantic import BaseModel

from fastapi import HTTPException, status


def python_type_to_sql_type(python_type):
    if python_type is Optional[int] or python_type is int:
        return '::INTEGER'
    elif python_type is Optional[str] or python_type is str:
        return '::VARCHAR'
    elif python_type is Optional[bool] or python_type is bool:
        return '::BOOLEAN'
    elif python_type is Optional[float] or python_type is float:
        return '::FLOAT'
    elif python_type is Optional[datetime.date] or python_type is datetime.date:
        return '::DATE'
    elif python_type is Optional[datetime.datetime] or python_type is datetime.datetime:
        return '::TIMESTAMP'
    return ''


def update_record(model: BaseModel or dict, table_name: str, record_id: int or str, id_field_name: str = "id"):
    if type(model) is not dict:
        model = model.dict(exclude_none=True)

    set_clauses = []
    values = []

    for field, value in model.items():
        python_type = type(value)
        data_type = python_type_to_sql_type(python_type)
        set_clauses.append(f"{field} = ${len(values) + 1}{data_type}")
        values.append(value)

    if not set_clauses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "ErrorCode.ValueError",
                "reason": "No fields to update"
            },
        )

    sql_query = f"UPDATE {table_name} SET " + ", ".join(set_clauses) + (f" WHERE {id_field_name} = ${len(values) + 1}"
                                                                        f"{python_type_to_sql_type(type(record_id))} "
                                                                        f"RETURNING *")
    values.append(record_id)
    return sql_query, *values


def insert_record(model: BaseModel or dict, table_name: str):
    if type(model) is not dict:
        model = model.dict(exclude_none=True)

    insert_fields = []
    set_clauses = []
    values = []

    for field, value in model.items():
        insert_fields.append(field)
        python_type = type(value)
        data_type = python_type_to_sql_type(python_type)
        set_clauses.append(f"${len(values) + 1}{data_type}")
        values.append(value)

    sql_query = (f"INSERT INTO {table_name} (" + ", ".join(insert_fields) + ") VALUES (" + ", ".join(set_clauses) +
                 ") RETURNING *")

    return sql_query, *values


def delete_record(table_name: str, record_id: int or str, id_field_name: str = "id"):
    sql_query = (f"DELETE FROM {table_name} WHERE {id_field_name} = $1{python_type_to_sql_type(type(record_id))} "
                 f"RETURNING *")

    return sql_query, record_id
