import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func

from app.database import Base


class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    enquiry_id = Column(String, ForeignKey("enquiries.id"))

    message_template = Column(Text, nullable=True)

    scheduled_at = Column(DateTime(timezone=True))

    completed = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
