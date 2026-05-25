from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.database import Base, engine

from app.routes.enquiry import router as enquiry_router
from app.routes.health import router as health_router

from app.utils.exceptions import (
    generic_exception_handler,
    validation_exception_handler
)

from app.middleware.request_logger import (
    RequestLoggingMiddleware
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Closira Backend Assignment",
    description="Async enquiry handling pipeline using FastAPI",
    version="1.0.0"
)


# Middleware
app.add_middleware(
    RequestLoggingMiddleware
)


# Exception Handlers
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)


# Routes
app.include_router(enquiry_router)
app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": "Closira backend is running"
    }


@app.on_event("startup")
def startup_event():

    print("Closira backend started successfully")