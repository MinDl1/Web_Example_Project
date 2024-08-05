from fastapi import (
    APIRouter,
    Response,
    Request,
    HTTPException,
    status,
)

from routes.auth.errors import ErrorCode
from routes.auth.utils.sql_utils import update_record
from routes.auth.config import user_table_name

from .utils import create_recovery_code
from .sql_querry import sql_id_select_one_email
from .models import ForgotPassword, ResetPassword


router = APIRouter()


@router.post(
    path="/forgot_password",
    summary="Request a reset password procedure",
    description="Sends a password recovery code by email",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=None,
)
async def forgot_password(
    request: Request,
    response: Response,
    forgot: ForgotPassword,
):
    postgres_email = await request.app.postgresql.fetchrow(sql_id_select_one_email, forgot.email)

    if not postgres_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.BAD_EMAIL,
                "reason": "Non-existent email in the application"
            },
        )

    recovery_code = create_recovery_code()
    await request.app.smtp.send_email(forgot.email, recovery_code)
    await request.app.redis.add_email_code(forgot.email, recovery_code)

    response.status_code = status.HTTP_200_OK
    return response


@router.post(
    path="/reset_password",
    summary="Reset a password",
    description="Reset a password by recovery code in email",
    response_description="HTTP 204 STATUS",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=None,
)
async def reset_password(
    request: Request,
    response: Response,
    reset: ResetPassword,
):
    recovery_code = await request.app.redis.get_email_code(reset.email)

    if not recovery_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.LACK_OF_EMAIL_IN_FORGOTTEN,
                "reason": f"Lack of email on the forgotten list"
            },
        )
    if recovery_code != reset.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.BAD_RECOVERY_CODE,
                "reason": f"Bad recovery code for input email"
            },
        )

    sql_user_update_password, *values = update_record(
        model={"password": reset.password},
        table_name=user_table_name,
        record_id=reset.email,
        id_field_name="email"
    )
    user = await request.app.postgresql.fetchrow(sql_user_update_password, *values)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.BAD_EMAIL,
                "reason": "Non-existent email in the application"
            },
        )

    request.app.redis.del_email_code(reset.email)

    response.status_code = status.HTTP_200_OK
    return response
