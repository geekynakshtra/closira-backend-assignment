from enum import Enum


class ChannelEnum(str, Enum):
    whatsapp = "whatsapp"
    email = "email"
    call = "call"


class EnquiryStatus(str, Enum):
    NEW = "new"
    PROCESSING = "processing"
    QUALIFIED = "qualified"
    ESCALATED = "escalated"
    FOLLOW_UP_SCHEDULED = "follow_up_scheduled"
