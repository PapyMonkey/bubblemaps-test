import httpx
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


def map_httpx_error(
    request: Request, exception: httpx.HTTPStatusError
) -> HTTPException:
    status = exception.response.status_code

    if status == 429:
        return HTTPException(status_code=429, detail="Rate limit from upstream")
    if 500 <= status < 600:
        return HTTPException(status_code=502, detail="Upstream server error")
    return HTTPException(status_code=503, detail=f"Upstream returned {status}")


async def httpx_status_exception_handler(
    request: Request, exception: httpx.HTTPStatusError
):
    http_exc = map_httpx_error(request, exception)
    return JSONResponse(
        status_code=http_exc.status_code, content={"detail": http_exc.detail}
    )


async def httpx_timeout_exception_handler(request: Request, exception: Exception):
    return JSONResponse(status_code=504, content={"detail": "Upstream timeout"})
