from pydantic import BaseModel, Field
from uuid import UUID

class UserCreate(BaseModel):
    id: UUID = Field(..., description="UUID assigned by Supabase Auth")
    full_name: str = Field(..., description="Full name of the user")
    role: str = Field(..., description="One of: admin, recepcionist, veterinary, client")

class UserOut(BaseModel):
    id: UUID
    full_name: str
    role: str

    model_config = {
        "from_attributes": True
    }