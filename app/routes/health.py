from fastapi import APIRouter
from sqlalchemy import text

from app.database import SessionLocal

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Application health check")
def health_check():

    db_status = "connected"

    try:
        db = SessionLocal()

        db.execute(text("SELECT 1"))

    except Exception:
        db_status = "disconnected"

    finally:
        db.close()

    return {"status": "healthy", "database": db_status}
