from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
from typing import List
from app.schemas.reviews import ReviewCreate, ReviewOut
from app.services.supabase_reviews import create_review, list_reviews_for_vet, list_reviews_by_owner
from app.auth.dependencies import get_current_user_id

router = APIRouter()

@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def create_review_endpoint(
    payload: ReviewCreate,
    owner_id: UUID = Depends(get_current_user_id)
):
    data = payload.dict()
    data["pet_owner_id"] = str(owner_id)
    rev = await create_review(data)
    return rev

@router.get("/vet/{vet_id}", response_model=List[ReviewOut])
async def list_reviews_vet(
    vet_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    
    from app.services.supabase_users import get_user_from_supabase
    current = await get_user_from_supabase(user_id)
    if current["role"] not in ("admin", "veterinario") or (current["role"]=="veterinario" and current["id"]!= str(vet_id)):
        raise HTTPException(status_code=403, detail="Not authorized")
    return await list_reviews_for_vet(vet_id)

@router.get("/owner", response_model=List[ReviewOut])
async def list_reviews_owner(
    owner_id: UUID = Depends(get_current_user_id)
):
    return await list_reviews_by_owner(owner_id)
