from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
from typing import List
from datetime import datetime
from app.schemas.appointment import AppointmentCreate, AppointmentOut
from app.services.supabase_appointments import (
    create_appointment, list_appointments, update_appointment, delete_appointment
)
from app.auth.dependencies import get_current_user_id

router = APIRouter()

@router.post("/", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
async def create_appointment_endpoint(
    payload: AppointmentCreate,
    client_id: UUID = Depends(get_current_user_id)
):
    data = payload.dict()
    data["client_id"] = str(client_id)
    appt = await create_appointment(data)
    return appt

@router.get("/", response_model=List[AppointmentOut])
async def list_appointments_endpoint(
    client_id: UUID = Depends(get_current_user_id)
):
    return await list_appointments({"client_id": str(client_id)})

@router.put("/{appointment_id}", response_model=AppointmentOut)
async def update_appointment_endpoint(
    appointment_id: UUID,
    payload: AppointmentCreate,
    user_id: UUID = Depends(get_current_user_id)
):
    
    data = payload.dict()
    updated = await update_appointment(appointment_id, data)
    return updated

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment_endpoint(
    appointment_id: UUID,
    client_id: UUID = Depends(get_current_user_id)
):
    success = await delete_appointment(appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Not found")
    return