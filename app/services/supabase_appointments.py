import os
from supabase import create_client, Client
from uuid import UUID
from typing import List

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_appointment(data: dict) -> dict:
    response = supabase.table("appointments").insert(data).execute()
    if response.status_code != 201:
        raise Exception(f"Error creating appointment: {response.error}")
    return response.data[0]

async def list_appointments(filter_data: dict) -> List[dict]:
    response = supabase.table("appointments").select("*").match(filter_data).execute()
    return response.data

async def update_appointment(appointment_id: UUID, data: dict) -> dict:
    response = supabase.table("appointments").update(data).eq("id", str(appointment_id)).execute()
    if response.error:
        raise Exception(f"Error updating: {response.error}")
    return response.data[0]

async def delete_appointment(appointment_id: UUID) -> bool:
    response = supabase.table("appointments").delete().eq("id", str(appointment_id)).execute()
    return response.status_code == 204