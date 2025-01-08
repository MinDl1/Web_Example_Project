import time
from datetime import datetime
from ipaddress import ip_address

from fastapi import Request, Response, status, Depends
from fastapi.responses import JSONResponse

from .jwt import get_user_id_from_jwt
from .models import LogsAPICreate, LogsAPI


async def api_logging(request: Request, call_next, postgres_session) -> Response:
    date_time = datetime.now()

    user_id = None
    authorization_header = request.headers.get('Authorization')
    if authorization_header and authorization_header.startswith('Bearer '):
        token = authorization_header[7:]
        user_id = get_user_id_from_jwt(token)
    if not user_id:
        refresh_token = request.cookies.get('refresh_token')
        if refresh_token:
            user_id = get_user_id_from_jwt(refresh_token)

    query_params = str(request.query_params) if request.query_params else None
    path_params = str(request.query_params) if request.path_params else None

    client_host = request.client.host

    logs_api = LogsAPICreate(
        id_user=user_id,
        client_host=client_host,
        client_port=request.client.port,
        url=request.url.path,
        method=request.method,
        query_params=query_params,
        path_params=path_params,
        api_date_time=date_time
    )

    db_logs_api = LogsAPI.model_validate(logs_api)
    postgres_session.add(db_logs_api)
    await postgres_session.commit()
    await postgres_session.refresh(db_logs_api)

    start_time = time.time()
    try:
        response = await call_next(request)
        response_error = response.headers.get("response-error")
    except Exception as e:
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": "Internal Server Error",
                "reason": "Internal Server Error"
            },
            headers={"response-error": "Internal Server Error"},
        )
        response_error = type(e).__module__ + '.' + type(e).__qualname__ + ' ' + str(e)
    end_time = time.time()
    execution_time = end_time - start_time

    logs_api.response_code = response.status_code
    logs_api.response_error = response_error
    logs_api.execution_time = execution_time

    db_logs_api.sqlmodel_update(logs_api)
    postgres_session.add(db_logs_api)
    await postgres_session.commit()

    return response
