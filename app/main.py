import httpx
from fastapi import FastAPI

from app import routes
from app.exceptions import (
    httpx_status_exception_handler,
    httpx_timeout_exception_handler,
)

bubblemaps = FastAPI()

bubblemaps.include_router(routes.router)

bubblemaps.add_exception_handler(httpx.HTTPStatusError, httpx_status_exception_handler)
bubblemaps.add_exception_handler(httpx.RequestError, httpx_timeout_exception_handler)
