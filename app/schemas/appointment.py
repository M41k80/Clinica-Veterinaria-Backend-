from pydantic import BaseModel, Field, condecimal
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class AppointmentCreate(BaseModel):
    pet_id: UUID = Field(...)
    vet_id: UUID = Field(...)
    scheduled_date: datetime
    start_time: datetime
    end_time: datetime
    services: Optional[List[str]] = Field(default=[])

class AppointmentOut(BaseModel):
    id: UUID
    pet_id: UUID
    client_id: UUID
    vet_id: UUID
    scheduled_date: datetime
    start_time: datetime
    end_time: datetime
    status: str
    services: Optional[List[str]]
    total_cost: Optional[condecimal(max_digits=10, decimal_places=2)]
    reminder_date: Optional[datetime]
    reminder_sent: bool
    created_at: datetime

    model_config = {"from_attributes": True}