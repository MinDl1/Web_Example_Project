from pydantic import BaseModel


class ForgotPassword(BaseModel):
    email: str


class ResetPassword(BaseModel):
    email: str
    code: str
    password: str
