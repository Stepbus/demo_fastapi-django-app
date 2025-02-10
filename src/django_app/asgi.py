"""
ASGI config for django_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

import django

from fastapi_app.errors import registered_errors

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.config.settings')

"""
Django settings
"""
django.setup()

from django.core.asgi import get_asgi_application
django_app = get_asgi_application()

"""
FastAPI settings
"""
from fastapi_app.routes.auth import auth_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi_app.routes.blocks import blocks_router

version = "v1"
fastapi_app = FastAPI(
    title="FastAPI and Django app",
    description="REST API for a test task",
    version=version,
    contact={"name": "Andrew",
             "email": "<aleksovs99@gmail.com>"},
)

registered_errors(fastapi_app)

# to mount Django
fastapi_app.mount("/static", StaticFiles(directory="django_app/static"), name="static")
fastapi_app.mount("/django", django_app)

# routes
fastapi_app.include_router(blocks_router, prefix=f"/api/{version}/block", tags=["blocks"])
fastapi_app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
