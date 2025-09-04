import os
from supabase import create_client, Client
from uuid import UUID

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_user_in_supabase(user_id: UUID, full_name: str, role: str):
    payload = {
        "id": str(user_id),
        "full_name": full_name,
        "role": role
    }
    response = supabase.table("users").insert(payload).execute()
    if response.status_code != 201:
        raise Exception(f"Error creating user: {response.data}")
    return response.data[0]

async def get_user_from_supabase(user_id: UUID):
    response = supabase.table("users").select("*").eq("id", str(user_id)).single().execute()
    if response.error:
        return None
    return response.data