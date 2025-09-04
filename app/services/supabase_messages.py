import os
from supabase import create_client, Client
from uuid import UUID
from typing import List

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def send_message(data: dict) -> dict:
    res = supabase.table("messages").insert(data).execute()
    if res.status_code != 201:
        raise Exception(res.error)
    return res.data[0]

async def list_messages(user_id: UUID, role: str) -> List[dict]:
    if role == 'cliente':
        # owners see sent and received
        res = supabase.table("messages").select("*").or_(
            f"sender_id.eq.{user_id},receiver_id.eq.{user_id}"
        ).execute()
    else:
        # vets see received only
        res = supabase.table("messages").select("*").eq("receiver_id", str(user_id)).execute()
    return res.data

async def mark_as_read(message_id: UUID) -> dict:
    res = supabase.table("messages").update({"is_read": True}).eq("id", str(message_id)).execute()
    if res.error:
        raise Exception(res.error)
    return res.data[0]