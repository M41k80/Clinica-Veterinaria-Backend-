from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List

class ScheduleCreate(BaseModel):
    vet_id: UUID = Field(..., description="UUID of veterinarian")
    start_time: datetime = Field(..., description="Start of working period")
    end_time: datetime = Field(..., description="End of working period")

class ScheduleOut(BaseModel):
    id: UUID
    vet_id: UUID
    start_time: datetime
    end_time: datetime
    is_available: bool

    model_config = {"from_attributes": True}

class TimeSlotOut(BaseModel):
    slot: datetime