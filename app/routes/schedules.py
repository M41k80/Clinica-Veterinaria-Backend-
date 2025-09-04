from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.schemas.schedule import ScheduleCreate, ScheduleOut, TimeSlotOut
from app.services.supabase_schedules import create_schedule, list_schedules, generate_time_slots
from app.auth.dependencies import get_current_user_id

router = APIRouter()

@router.post("/", response_model=ScheduleOut, status_code=status.HTTP_201_CREATED)
async def create_schedule_endpoint(
    payload: ScheduleCreate,
    vet_id: UUID = Depends(get_current_user_id)
):
    if vet_id != payload.vet_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await create_schedule(payload.vet_id, payload.start_time.isoformat(), payload.end_time.isoformat())

@router.get("/", response_model=list[ScheduleOut])
async def list_schedules_endpoint(
    vet_id: UUID = Depends(get_current_user_id)
):
    return await list_schedules(vet_id)

@router.get("/slots", response_model=list[TimeSlotOut])
async def get_time_slots_endpoint(
    vet_id: UUID = Depends(get_current_user_id)
):
    return await generate_time_slots(vet_id)