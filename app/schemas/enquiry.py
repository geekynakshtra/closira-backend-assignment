from pydantic import BaseModel, Field

from app.utils.enums import ChannelEnum


class EnquiryCreate(BaseModel):

    customer_name: str = Field(..., example="Sarah Johnson")

    channel: ChannelEnum = Field(..., example="whatsapp")

    message: str = Field(..., example="Need pricing details for premium plan")


class EnquiryResponse(BaseModel):

    id: str

    status: str

    message: str

    class Config:
        from_attributes = True
