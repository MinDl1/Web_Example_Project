from fastapi import (
    APIRouter,
    Depends,
    Request,
    status,
)
from typing import Annotated, List

from routes.auth.ident.models import User
from routes.auth.ident.manager import get_current_active_user

from .models import Endpoint
from .sql_query import sql_endpoints_select_all
from .responses import all_endpoints_get_responses


router = APIRouter()


@router.get(
    path="/all",
    summary="Shows list of all endpoints",
    description="Shows list of all endpoints",
    response_description="List of all endpoints",
    status_code=status.HTTP_200_OK,
    response_model=List[Endpoint],
    responses=all_endpoints_get_responses,
)
async def read_endpoints(
    current_user: Annotated[User, Depends(get_current_active_user)],
    request: Request
) -> List[Endpoint]:
    async with request.app.postgresql.acquire() as postgres_conn:
        users = await postgres_conn.fetch(sql_endpoints_select_all)

    return [Endpoint.model_validate(dict(row)) for row in users]
