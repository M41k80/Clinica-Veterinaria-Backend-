from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
from typing import List
from app.schemas.service import ServiceCreate, ServiceOut
from app.services.supabase_services import (
    create_service,
    list_services,
    get_service,
    update_service,
    delete_service
)
from app.auth.dependencies import get_current_user_id

router = APIRouter()

@router.post("/", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
async def create_service_endpoint(
    payload: ServiceCreate,
    user_id: UUID = Depends(get_current_user_id)
):
    # Only admin or receptionist can create services
    from app.services.supabase_users import get_user_from_supabase
    current = await get_user_from_supabase(user_id)
    if current["role"] not in ("admin", "recepcionista"):
        raise HTTPException(status_code=403, detail="Not authorized")
    service = await create_service(payload.name, payload.description, float(payload.price))
    return service

@router.get("/", response_model=List[ServiceOut])
async def list_services_endpoint():
    return await list_services()

@router.get("/{service_id}", response_model=ServiceOut)
async def get_service_endpoint(service_id: UUID):
    service = await get_service(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/{service_id}", response_model=ServiceOut)
async def update_service_endpoint(
    service_id: UUID,
    payload: ServiceCreate,
    user_id: UUID = Depends(get_current_user_id)
):
    from app.services.supabase_users import get_user_from_supabase
    current = await get_user_from_supabase(user_id)
    if current["role"] not in ("admin", "recepcionista"):
        raise HTTPException(status_code=403, detail="Not authorized")
    data = payload.dict()
    updated = await update_service(service_id, data)
    return updated

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_endpoint(
    service_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    from app.services.supabase_users import get_user_from_supabase
    current = await get_user_from_supabase(user_id)
    if current["role"] not in ("admin", "recepcionista"):
        raise HTTPException(status_code=403, detail="Not authorized")
    success = await delete_service(service_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")
    return
