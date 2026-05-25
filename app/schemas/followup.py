from typing import Optional

from pydantic import BaseModel, Field


class FollowUpCreate(BaseModel):

    delay_minutes: int = Field(..., example=30)

    message_template: Optional[str] = Field(
        default=None, example="Checking in regarding your enquiry"
    )
