from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.event_logger import create_event
from app.models.enquiry import Enquiry
from app.utils.enums import EnquiryStatus


def create_enquiry(db: Session, customer_name: str, channel: str, message: str):

    enquiry = Enquiry(
        customer_name=customer_name,
        channel=channel,
        message=message,
        status=EnquiryStatus.NEW.value,
    )

    db.add(enquiry)

    db.commit()

    db.refresh(enquiry)

    create_event(db, enquiry.id, "created", "Enquiry created successfully")

    return enquiry


def get_enquiry_or_404(db: Session, enquiry_id: str):

    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()

    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")

    return enquiry
