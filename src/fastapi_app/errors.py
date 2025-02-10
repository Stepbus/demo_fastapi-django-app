from typing import Callable, Coroutine, Any

from fastapi import FastAPI, status
from fastapi.requests import Request
from starlette.responses import JSONResponse


class ProjectException(Exception):
    """This is the base class for all project errors"""
    pass


class InsufficientPermission(ProjectException):
    """User does not have the necessary permissions to perform an action."""
    pass


def create_exception_handler(
        status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]:
    async def exception_handler(request: Request, exc: ProjectException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def registered_errors(app: FastAPI):
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )
