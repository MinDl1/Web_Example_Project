from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Request, Response
from jose import JWTError, jwt

from .models import TokenData
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS
from .sql_querry import sql_user_select_one_id
from routes.auth.user.models import User


def create_access_token(data: dict):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if access_token_expires:
        expire = datetime.now(timezone.utc) + access_token_expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, response: Response):
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    if refresh_token_expires:
        expire = datetime.now(timezone.utc) + refresh_token_expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    response.set_cookie(
        key="refresh_token",
        value=encoded_jwt,
        expires=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        secure=False,
        httponly=True,
    )


async def verify_token(token: str, request: Request) -> TokenData:
    invalid_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_u: str = payload.get("id")
        if id_u is None:
            raise invalid_token_exception
        user = await request.app.postgresql.fetchrow(sql_user_select_one_id, id_u)
        if user is None:
            raise invalid_token_exception
        return TokenData.from_dict(dict(user))
    except JWTError:
        raise invalid_token_exception


async def verify_access_token(token: str, request: Request) -> User or bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_u: str = payload.get("id")
        if id_u is None:
            return False
        user = await request.app.postgresql.fetchrow(sql_user_select_one_id, id_u)
        if user is None:
            return False
        return User.from_dict(dict(user))
    except JWTError:
        return False
