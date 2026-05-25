from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "errors": exc.errors(),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500, content={"success": False, "message": "Internal server error"}
    )
