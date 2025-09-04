import os
from supabase import create_client, Client
from uuid import UUID
from typing import List

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_review(data: dict) -> dict:
    res = supabase.table("reviews").insert(data).execute()
    if res.status_code != 201:
        raise Exception(res.error)
    return res.data[0]

async def list_reviews_for_vet(vet_id: UUID) -> List[dict]:
    res = supabase.table("reviews").select("*").eq("veterinarian_id", str(vet_id)).execute()
    return res.data

async def list_reviews_by_owner(owner_id: UUID) -> List[dict]:
    res = supabase.table("reviews").select("*").eq("pet_owner_id", str(owner_id)).execute()
    return res.data