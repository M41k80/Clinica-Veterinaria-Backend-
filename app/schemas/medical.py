from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date

class VaccineRecordCreate(BaseModel):
    name: str = Field(..., description="Vaccine name")
    applied_date: date = Field(..., description="Date of application")
    next_dose_date: date | None = Field(None, description="Next dose date")

class TreatmentRecordCreate(BaseModel):
    name: str = Field(..., description="Treatment name")
    details: str = Field(..., description="Treatment details")
    start_date: date = Field(..., description="Start date of treatment")

class MedicalRecordCreate(BaseModel):
    appointment_id: UUID = Field(..., description="Linked appointment UUID")
    pet_id: UUID = Field(..., description="Linked pet UUID")
    veterinarian_id: UUID = Field(..., description="Veterinarian UUID")
    diagnosis: str = Field(..., description="Diagnosis text")
    notes: str | None = Field(None, description="Additional notes")
    vaccines: list[VaccineRecordCreate] = Field(default_factory=list)
    treatments: list[TreatmentRecordCreate] = Field(default_factory=list)

class VaccineRecordOut(VaccineRecordCreate):
    id: UUID
    medical_record_id: UUID

class TreatmentRecordOut(TreatmentRecordCreate):
    id: UUID
    medical_record_id: UUID

class MedicalRecordOut(BaseModel):
    id: UUID
    appointment_id: UUID
    pet_id: UUID
    veterinarian_id: UUID
    diagnosis: str
    notes: str | None
    vaccines: list[VaccineRecordOut]
    treatments: list[TreatmentRecordOut]

    model_config = {"from_attributes": True}
