import os
from supabase import create_client, Client
from uuid import UUID

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_medical_record(data: dict) -> dict:
    resp = supabase.table("medical_records").insert(data).execute()
    if resp.status_code != 201:
        raise Exception(resp.error)
    return resp.data[0]

async def create_vaccine_record(data: dict) -> dict:
    resp = supabase.table("vaccine_records").insert(data).execute()
    if resp.status_code != 201:
        raise Exception(resp.error)
    return resp.data[0]

async def create_treatment_record(data: dict) -> dict:
    resp = supabase.table("treatment_records").insert(data).execute()
    if resp.status_code != 201:
        raise Exception(resp.error)
    return resp.data[0]

async def get_medical_record(record_id: UUID) -> dict | None:
    resp = supabase.table("medical_records").select("*").eq("id", str(record_id)).single().execute()
    return resp.data
