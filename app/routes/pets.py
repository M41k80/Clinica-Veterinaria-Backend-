from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
from app.schemas.pet import PetCreate, PetOut
from app.services.supabase_pets import create_pet, list_pets, get_pet, update_pet, delete_pet
from app.auth.dependencies import get_current_user_id

router = APIRouter()

@router.post("/", response_model=PetOut, status_code=status.HTTP_201_CREATED)
async def create_pet_endpoint(
    pet: PetCreate,
    current_user_id: UUID = Depends(get_current_user_id)
):
    created = await create_pet(pet.name, pet.breed, pet.age, current_user_id)
    return created

@router.get("/", response_model=list[PetOut])
async def list_pets_endpoint(
    current_user_id: UUID = Depends(get_current_user_id)
):
    return await list_pets(current_user_id)

@router.get("/{pet_id}", response_model=PetOut)
async def get_pet_endpoint(
    pet_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id)
):
    pet = await get_pet(pet_id, current_user_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@router.put("/{pet_id}", response_model=PetOut)
async def update_pet_endpoint(
    pet_id: UUID,
    pet: PetCreate,
    current_user_id: UUID = Depends(get_current_user_id)
):
    updated = await update_pet(pet_id, current_user_id, pet.name, pet.breed, pet.age)
    if not updated:
        raise HTTPException(status_code=404, detail="Pet not found or not authorized to update")
    return updated

@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet_endpoint(
    pet_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id)
):
    success = await delete_pet(pet_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pet not found or not authorized to delete")
