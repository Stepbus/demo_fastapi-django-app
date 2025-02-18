from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str


class UserResponseSchema(BaseModel):
    username: str
    email: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str
