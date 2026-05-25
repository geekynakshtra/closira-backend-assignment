import uuid

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    customer_name = Column(String, nullable=False)

    channel = Column(String, nullable=False)

    message = Column(Text, nullable=False)

    status = Column(String, default="new")

    matched_sop = Column(String, nullable=True)

    suggested_response = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
