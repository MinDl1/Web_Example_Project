from passlib.context import CryptContext

from .models import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: dict, password: str) -> TokenData or bool:
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return TokenData.from_dict(user)
