from fastapi import APIRouter, HTTPException, Depends, status
from uuid import UUID
from typing import List
from app.schemas.message import MessageCreate, MessageOut
from app.services.supabase_messages import send_message, list_messages, mark_as_read
from app.auth.dependencies import get_current_user_id
from app.services.supabase_users import get_user_from_supabase

router = APIRouter()

@router.post("/", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def send_message_endpoint(
    payload: MessageCreate,
    user_id: UUID = Depends(get_current_user_id)
):
    
    sender = await get_user_from_supabase(user_id)
    if sender["role"] != "cliente":
        raise HTTPException(status_code=403, detail="Only pet owners can send messages")
    data = payload.dict()
    data["sender_id"] = str(user_id)
    msg = await send_message(data)
    return msg

@router.get("/", response_model=List[MessageOut])
async def list_messages_endpoint(
    user_id: UUID = Depends(get_current_user_id)
):
    user = await get_user_from_supabase(user_id)
    msgs = await list_messages(user_id, user["role"])
    return msgs

@router.patch("/{message_id}/read", response_model=MessageOut)
async def mark_read_endpoint(
    message_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    user = await get_user_from_supabase(user_id)
    if user["role"] != "veterinario":
        raise HTTPException(status_code=403, detail="Only veterinarians can mark messages read")
    msg = await mark_as_read(message_id)
    return msg