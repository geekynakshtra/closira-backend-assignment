import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func

from app.database import Base


class EnquiryEvent(Base):
    __tablename__ = "enquiry_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    enquiry_id = Column(String, ForeignKey("enquiries.id"))

    event_type = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
