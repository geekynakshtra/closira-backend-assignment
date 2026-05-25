import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import log_event


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        response = await call_next(request)

        duration = round(time.time() - start_time, 4)

        log_event(
            {
                "event": "request",
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration": duration,
            }
        )

        return response
