import jwt
from django.contrib.auth.models import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from fastapi_app.errors import InsufficientPermission
from fastapi_app.settings import Config
from fastapi_app.utils import verify_token

SECRET_KEY = Config.SECRET_KEY
JWT_ALGORITHM = Config.JWT_ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Retrieves the current authenticated user from JWT.
    """
    try:
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        username: str = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid authentication token: Missing user field")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.is_active:
            raise InsufficientPermission()

        return user

    except (PyJWTError, User.DoesNotExist) as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication token: {e}")
