from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_app.dependencies import get_current_user
from fastapi_app.schemas import UserRegisterSchema, TokenSchema
from fastapi_app.schemas.auth import UserResponseSchema
from fastapi_app.utils import create_access_token, create_refresh_token, verify_token

auth_router = APIRouter()


@auth_router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegisterSchema):
    """
    Creates a new user account.
    """
    try:
        user = User.objects.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            is_active=True,
        )
        return UserResponseSchema(username=user.username, email=user.email)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or Email already exists")


@auth_router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns access & refresh tokens.
    """
    user = authenticate(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@auth_router.post("/refresh", response_model=TokenSchema)
def refresh_token(refresh_token: str):
    """
    Refreshes the access token if the refresh token is valid.
    """
    payload = verify_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token type")

    username = payload.get("sub")

    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(username)
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@auth_router.get("/me", response_model=UserResponseSchema)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Returns information about the currently authenticated user.
    """
    return UserResponseSchema(username=current_user.username, email=current_user.email)
