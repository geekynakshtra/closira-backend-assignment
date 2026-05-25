from sqlalchemy.orm import Session

from app.core.event_logger import create_event
from app.models.enquiry import Enquiry
from app.services.sop_matcher import match_sop
from app.utils.enums import EnquiryStatus
from app.utils.logger import log_event


def process_enquiry(enquiry_id: str, db: Session):

    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()

    if not enquiry:
        return

    enquiry.status = EnquiryStatus.PROCESSING.value

    db.commit()

    create_event(db, enquiry.id, "processing_started", "Background processing started")

    result = match_sop(enquiry.message)

    if result["matched"]:

        enquiry.status = EnquiryStatus.QUALIFIED.value

        enquiry.matched_sop = result["sop"]

        enquiry.suggested_response = result["response"]

        db.commit()

        create_event(db, enquiry.id, "sop_matched", f"SOP matched: {result['sop']}")

        log_event(
            {"event": "sop_matched", "enquiry_id": enquiry.id, "sop": result["sop"]}
        )

    else:

        enquiry.status = EnquiryStatus.ESCALATED.value

        db.commit()

        create_event(
            db, enquiry.id, "escalated", "No SOP matched. Escalated to human agent."
        )

        log_event({"event": "escalated", "enquiry_id": enquiry.id})
