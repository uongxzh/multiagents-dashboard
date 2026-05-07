from typing import Any, Generic, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar("T")


class ErrorBody(BaseModel):
    code: str
    message: str


class ApiResponse(BaseModel, Generic[T]):
    data: T | None = None
    error: ErrorBody | None = None


def ok(data: Any = None) -> ApiResponse:
    return ApiResponse(data=data, error=None)


def err(code: str, message: str, status_code: int = 200) -> JSONResponse:
    body = ApiResponse(data=None, error=ErrorBody(code=code, message=message))
    return JSONResponse(status_code=status_code, content=body.model_dump())
