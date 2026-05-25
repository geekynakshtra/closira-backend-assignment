from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.core.event_logger import create_event
from app.database import get_db
from app.models.enquiry_event import EnquiryEvent
from app.models.followup import FollowUp
from app.schemas.enquiry import EnquiryCreate, EnquiryResponse
from app.schemas.escalation import EscalationRequest
from app.schemas.followup import FollowUpCreate
from app.services.enquiry_service import create_enquiry, get_enquiry_or_404
from app.utils.enums import EnquiryStatus
from app.workers.enquiry_worker import process_enquiry

router = APIRouter(prefix="/enquiry", tags=["Enquiries"])


@router.post(
    "", response_model=EnquiryResponse, status_code=201, summary="Create new enquiry"
)
def create_new_enquiry(
    payload: EnquiryCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):

    enquiry = create_enquiry(
        db, payload.customer_name, payload.channel, payload.message
    )

    background_tasks.add_task(process_enquiry, enquiry.id, db)

    return {
        "id": enquiry.id,
        "status": enquiry.status,
        "message": "Enquiry created successfully",
    }


@router.post("/{enquiry_id}/follow-up", summary="Schedule follow-up")
def schedule_followup(
    enquiry_id: str, payload: FollowUpCreate, db: Session = Depends(get_db)
):

    enquiry = get_enquiry_or_404(db, enquiry_id)

    scheduled_time = datetime.utcnow() + timedelta(minutes=payload.delay_minutes)

    followup = FollowUp(
        enquiry_id=enquiry.id,
        message_template=payload.message_template,
        scheduled_at=scheduled_time,
    )

    db.add(followup)

    enquiry.status = EnquiryStatus.FOLLOW_UP_SCHEDULED.value

    db.commit()

    create_event(
        db,
        enquiry.id,
        "followup_scheduled",
        f"Follow-up scheduled in {payload.delay_minutes} minutes",
    )

    return {"message": "Follow-up scheduled successfully"}


@router.post("/{enquiry_id}/escalate", summary="Escalate enquiry")
def escalate_enquiry(
    enquiry_id: str, payload: EscalationRequest, db: Session = Depends(get_db)
):

    enquiry = get_enquiry_or_404(db, enquiry_id)

    enquiry.status = EnquiryStatus.ESCALATED.value

    db.commit()

    create_event(db, enquiry.id, "escalated", payload.reason)

    return {"message": "Enquiry escalated successfully"}


@router.get("/{enquiry_id}/history", summary="Get enquiry history")
def get_history(enquiry_id: str, db: Session = Depends(get_db)):

    enquiry = get_enquiry_or_404(db, enquiry_id)

    events = db.query(EnquiryEvent).filter(EnquiryEvent.enquiry_id == enquiry.id).all()

    followups = db.query(FollowUp).filter(FollowUp.enquiry_id == enquiry.id).all()

    return {"enquiry": enquiry, "timeline": events, "followups": followups}
