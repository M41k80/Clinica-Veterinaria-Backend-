from pydantic import BaseModel, Field
from typing import Optional, Tuple
from datetime import datetime, date

class ServiceBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    date_range: Optional[Tuple[date, date]] = None  # Representa el rango de fechas como una tupla

class ServiceCreate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
