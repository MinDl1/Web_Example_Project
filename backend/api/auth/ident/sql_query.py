from sqlmodel import (
    select,
    case,
    and_,
    func,
    bindparam,
)

from ..role.models import Role, RoleRight
from ..user.models import User, UserRight
from ..tag_endpoint.models import Endpoint

from .config import SQLQueryParam


class SQLQuery:
    """

    """
    user_one_username = (
        select(
            User.id.label(SQLQueryParam.id_user),
            case(
                (User.id_extra_role.is_(None), User.id_base_role),
                (
                    func.now()
                    .between(User.date_start_extra_role, User.date_stop_extra_role),
                    User.id_extra_role
                ),
                else_=User.id_base_role
            ).label(SQLQueryParam.id_role),
            User.is_active,
            User.hashed_password,
        )
        .where(
            and_(
                User.username == bindparam(SQLQueryParam.username),
                User.is_deleted == False
            )
        )
        .limit(1)
    )

    user_one_id = (
        select(
            User.id.label(SQLQueryParam.id_user),
            case(
                (User.id_extra_role.is_(None), User.id_base_role),
                (
                    func.now()
                    .between(User.date_start_extra_role, User.date_stop_extra_role),
                    User.id_extra_role
                ),
                else_=User.id_base_role
            ).label(SQLQueryParam.id_role),
            User.is_active,
        )
        .where(
            and_(
                User.id == bindparam(SQLQueryParam.id_user),
                User.is_deleted == False
            )
        )
    )

    user_one_right = (
        select(
            User.id.label(SQLQueryParam.id_user),
            case(
                (User.id_extra_role.is_(None), User.id_base_role),
                (
                    func.now()
                    .between(User.date_start_extra_role, User.date_stop_extra_role),
                    User.id_extra_role
                ),
                else_=User.id_base_role
            ).label(SQLQueryParam.id_role),
            User.is_active,
            UserRight.is_allow,
        )
        .join(
            UserRight,
            UserRight.id_user == User.id
        )
        .where(
            and_(
                User.id == bindparam(SQLQueryParam.id_user),
                UserRight.id_endpoint == bindparam(SQLQueryParam.id_endpoint),
                User.is_deleted == False
            )
        )
        .limit(1)
    )

    user_one_role_right = (
        select(
            User.id.label(SQLQueryParam.id_user),
            RoleRight.id_role.label(SQLQueryParam.id_role),
            User.is_active,
        )
        .join(
            RoleRight,
            RoleRight.id_role == case(
                (User.id_extra_role.is_(None), User.id_base_role),
                (
                    func.now()
                    .between(User.date_start_extra_role, User.date_stop_extra_role),
                    User.id_extra_role
                ),
                else_=User.id_base_role
            )
        )
        .join(
            Role,
            Role.id == RoleRight.id_role
        )
        .where(
            and_(
                User.id == bindparam(SQLQueryParam.id_user),
                RoleRight.id_endpoint == bindparam(SQLQueryParam.id_endpoint),
                User.is_deleted == False,
                Role.is_active == True,
                Role.is_deleted == False
            )
        )
        .limit(1)
    )

    endpoint_one = (
        select(
            Endpoint.id
        ).where(
            and_(
                Endpoint.url == bindparam(SQLQueryParam.url),
                Endpoint.method == bindparam(SQLQueryParam.method))
        )
    )
