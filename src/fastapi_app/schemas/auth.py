from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
