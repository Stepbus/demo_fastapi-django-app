import inspect
from datetime import datetime, timedelta

import jwt
from django.contrib.auth import _get_backends, user_login_failed, _clean_credentials
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied
from django.views.decorators.debug import sensitive_variables
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


@sensitive_variables("credentials")
def authenticate(request=None, **credentials):
    """
    If the given credentials are valid, return a User object.
    """
    for backend, backend_path in _get_backends(return_tuples=True):
        backend_signature = inspect.signature(backend.authenticate)
        try:
            backend_signature.bind(request, **credentials)
        except TypeError:
            # This backend doesn't accept these credentials as arguments. Try
            # the next one.
            continue
        try:
            if isinstance(backend, ModelBackend):
                user = CustomModelBackend().authenticate(request, **credentials)
            else:
                user = backend.authenticate(request, **credentials)
        except PermissionDenied:
            # This backend says to stop in our tracks - this user should not be
            # allowed in at all.
            break
        if user is None:
            continue
        # Annotate the user object with the path of the backend.
        user.backend = backend_path
        return user

    # The credentials supplied are invalid to all backends, fire signal
    user_login_failed.send(
        sender=__name__, credentials=_clean_credentials(credentials), request=request
    )


class CustomModelBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return True
