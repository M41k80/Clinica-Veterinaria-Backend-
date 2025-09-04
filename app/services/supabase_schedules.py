import os
from supabase import create_client, Client
from uuid import UUID
from datetime import timedelta

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_schedule(vet_id: UUID, start: str, end: str) -> dict:
    payload = {"vet_id": str(vet_id), "start_time": start, "end_time": end}
    res = supabase.table("schedules").insert(payload).execute()
    if res.status_code != 201:
        raise Exception(res.error)
    return res.data[0]

async def list_schedules(vet_id: UUID) -> list[dict]:
    res = supabase.table("schedules").select("*").eq("vet_id", str(vet_id)).execute()
    return res.data

async def generate_time_slots(vet_id: UUID) -> list[dict]:
    schedules = await list_schedules(vet_id)
    slots = []
    for s in schedules:
        start = s["start_time"]
        end = s["end_time"]
        current = start
        while current + timedelta(minutes=30) <= end:
            slots.append({"slot": current})
            current += timedelta(minutes=30)
    return slots