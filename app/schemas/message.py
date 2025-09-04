from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class MessageCreate(BaseModel):
    sender_id: UUID = Field(..., description="UUID of the pet owner sending the message")
    receiver_id: UUID = Field(..., description="UUID of the veterinarian receiving the message")
    content: str = Field(..., description="Content of the message")

class MessageOut(BaseModel):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str
    timestamp: datetime
    is_read: bool

    model_config = {"from_attributes": True}