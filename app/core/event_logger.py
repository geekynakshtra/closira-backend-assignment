from sqlalchemy.orm import Session

from app.models.enquiry_event import EnquiryEvent


def create_event(db: Session, enquiry_id: str, event_type: str, description: str):

    event = EnquiryEvent(
        enquiry_id=enquiry_id, event_type=event_type, description=description
    )

    db.add(event)

    db.commit()

    db.refresh(event)

    return event
