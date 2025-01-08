issuer = "Web_Example_project"
"""JWT issuer."""


class TokenName:
    """Token name in enum .jwt.TokenSpec.

    Attributes:
        ACCESS_TOKEN: Access token.
        REFRESH_TOKEN: Refresh token.
    """
    ACCESS_TOKEN = "ACCESS_TOKEN"
    REFRESH_TOKEN = "REFRESH_TOKEN"


class SQLQueryParam:
    """SQL bind param that use in .sql_query.SQLQuery and .model.TokenData.

    Attributes:
        username: Username.
        id_user: ID user.
        id_role: ID role.
        id_endpoint: ID endpoint.
        url: Endpoint url.
        method: Endpoint method.
    """
    username = "username"
    id_user = "sub"
    id_role = "roles"
    # id_groups = "groups"
    id_endpoint = "id_endpoint"
    url = "url"
    method = "method"


IDENT_TAG = "auth"
"""Swagger ident tag"""


class IdentUrl:
    """Url in ident tag.

    Attributes:
        LOGIN: Login in system.
        REFRESH_TOKEN: Refresh access token by refresh token.
        LOGOUT: Logout.
    """
    LOGIN = "/login"
    REFRESH_TOKEN = "/refresh_token"
    LOGOUT = "/logout"
