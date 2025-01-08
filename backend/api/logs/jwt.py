from jose import jwt, JWTError
from pydantic import ValidationError

from config import (
    SECRET_KEY,
    ALGORITHM,
)
from auth.ident.models import TokenData


def get_user_id_from_jwt(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData.model_validate(payload)
        return token_data.id
    except ValidationError:
        return None
    except JWTError:
        return None
