from typing import List, Optional

from pydantic import BaseModel


class EventResponse(BaseModel):

    event_type: str

    description: str

    created_at: str

    class Config:
        from_attributes = True


class FollowupResponse(BaseModel):

    id: str

    message_template: Optional[str]

    completed: bool

    class Config:
        from_attributes = True


class EnquiryHistoryResponse(BaseModel):

    id: str

    customer_name: str

    status: str

    matched_sop: Optional[str]

    suggested_response: Optional[str]

    timeline: List[EventResponse]

    followups: List[FollowupResponse]
