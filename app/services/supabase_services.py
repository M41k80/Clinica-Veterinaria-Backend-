import os
from supabase import create_client, Client
from uuid import UUID

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_service(name: str, description: str | None, price: float) -> dict:
    payload = {
        "name": name,
        "description": description,
        "price": price
    }
    response = supabase.table("services").insert(payload).execute()
    if response.status_code != 201:
        raise Exception(f"Error creating service: {response.error}")
    return response.data[0]

async def list_services() -> list[dict]:
    response = supabase.table("services").select("*").execute()
    return response.data

async def get_service(service_id: UUID) -> dict | None:
    response = supabase.table("services").select("*").eq("id", str(service_id)).single().execute()
    if response.error:
        return None
    return response.data

async def update_service(service_id: UUID, data: dict) -> dict:
    response = supabase.table("services").update(data).eq("id", str(service_id)).execute()
    if response.error:
        raise Exception(f"Error updating service: {response.error}")
    return response.data[0]

async def delete_service(service_id: UUID) -> bool:
    response = supabase.table("services").delete().eq("id", str(service_id)).execute()
    return response.status_code == 204
