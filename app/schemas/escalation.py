from pydantic import BaseModel, Field


class EscalationRequest(BaseModel):

    reason: str = Field(..., example="Customer requested human support")
