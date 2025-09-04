from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.schemas.medical import (
    MedicalRecordCreate, MedicalRecordOut,
    VaccineRecordCreate, VaccineRecordOut,
    TreatmentRecordCreate, TreatmentRecordOut
)
from app.services.supabase_medical import (
    create_medical_record,
    create_vaccine_record,
    create_treatment_record,
    get_medical_record
)
from app.auth.dependencies import get_current_user_id

router = APIRouter()

@router.post("/", response_model=MedicalRecordOut, status_code=status.HTTP_201_CREATED)
async def create_medical_record_endpoint(
    payload: MedicalRecordCreate,
    vet_id: UUID = Depends(get_current_user_id)
):
    # primero inserta el record principal
    data = {
        "appointment_id": str(payload.appointment_id),
        "pet_id": str(payload.pet_id),
        "veterinarian_id": str(vet_id),
        "diagnosis": payload.diagnosis,
        "notes": payload.notes
    }
    mr = await create_medical_record(data)

    
    vaccines_out = []
    for v in payload.vaccines:
        vdata = {**v.dict(), "medical_record_id": mr["id"]}
        vaccines_out.append(await create_vaccine_record(vdata))

    treatments_out = []
    for t in payload.treatments:
        tdata = {**t.dict(), "medical_record_id": mr["id"]}
        treatments_out.append(await create_treatment_record(tdata))

    return {
        **mr,
        "vaccines": vaccines_out,
        "treatments": treatments_out
    }

@router.get("/{record_id}", response_model=MedicalRecordOut)
async def read_medical_record(
    record_id: UUID,
    vet_id: UUID = Depends(get_current_user_id)
):
    mr = await get_medical_record(record_id)
    if not mr:
        raise HTTPException(status_code=404, detail="Not found")
    return mr
