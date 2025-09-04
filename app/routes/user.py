from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
from app.schemas.user import UserCreate, UserOut
from app.services.supabase_users import create_user_in_supabase, get_user_from_supabase
from app.auth.dependencies import get_current_user_id

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    current_user_id: UUID = Depends(get_current_user_id)
):
    
    existing = await get_user_from_supabase(payload.id)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    current = await get_user_from_supabase(current_user_id)
   
    if current["role"] != "admin" and current_user_id != payload.id:
        raise HTTPException(status_code=403, detail="Not authorized to create this user")

    created = await create_user_in_supabase(payload.id, payload.full_name, payload.role)
    return created

@router.get("/{user_id}", response_model=UserOut)
async def read_user(
    user_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id)
):
    user = await get_user_from_supabase(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user_id != user_id:
        current = await get_user_from_supabase(current_user_id)
        if current["role"] != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to view this user")
    return user