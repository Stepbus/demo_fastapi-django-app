from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from fastapi_app.settings import Config

SECRET_KEY = Config.SECRET_KEY
JWT_ALGORITHM = Config.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(username: str) -> str:
    """
    Creates a JWT token for the authenticated user.
    """
    expiration_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": username,
        "exp": expiration_time.timestamp(),
        "type": "access"
    }
    return jwt.encode(token_data, SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(username: str) -> str:
    """
    Creates a JWT refresh token (longer-lived).
    """
    expiration_time = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token_data = {
        "sub": username,
        "exp": expiration_time.timestamp(),
        "type": "refresh"
    }
    return jwt.encode(token_data, SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str):
    """
    Verifies and decodes a JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])

        if "sub" not in payload or "exp" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
