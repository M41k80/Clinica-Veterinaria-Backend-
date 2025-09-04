from pydantic import BaseModel, Field
from uuid import UUID

class PetCreate(BaseModel):
    name: str = Field(..., description="Pet's name")
    breed: str = Field(..., description="Pet's breed")
    age: int = Field(..., ge=0, description="Pet's age in years")
    gender: str = Field(..., description="Pet's gender")
    pet_owner: UUID = Field(..., description="Pet's owner")

class PetOut(BaseModel):
    id: UUID
    name: str
    breed: str
    age: int
    pet_owner: UUID

    model_config = {
        "from_attributes": True
    }