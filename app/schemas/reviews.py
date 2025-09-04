from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class ReviewCreate(BaseModel):
    veterinarian_id: UUID = Field(..., description="UUID of the veterinarian being rated")
    appointment_id: UUID = Field(..., description="UUID of the related appointment")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str | None = Field(None, description="Optional review comment")

class ReviewOut(BaseModel):
    id: UUID
    veterinarian_id: UUID
    pet_owner_id: UUID
    appointment_id: UUID
    rating: int
    comment: str | None
    timestamp: datetime

    model_config = {"from_attributes": True}