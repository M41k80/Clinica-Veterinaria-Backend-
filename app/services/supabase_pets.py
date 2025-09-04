import os
from supabase import create_client, Client
from uuid import UUID

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def create_pet(name: str, breed: str, age: int, owner_id: UUID):
    payload = {
        "name": name,
        "breed": breed,
        "age": age,
        "pet_owner": str(owner_id)
    }
    response = supabase.table("pets").insert(payload).execute()
    if response.status_code != 201:
        raise Exception(f"Error creating pet: {response.data}")
    return response.data[0]

async def list_pets(owner_id: UUID):
    response = supabase.table("pets").select("*").eq("pet_owner", str(owner_id)).execute()
    return response.data

async def get_pet(pet_id: UUID, owner_id: UUID):
    response = supabase.table("pets").select("*").match({"id": str(pet_id), "pet_owner": str(owner_id)}).single().execute()
    return response.data

async def update_pet(pet_id: UUID, owner_id: UUID, name: str, breed: str, age: int):
    payload = {"name": name, "breed": breed, "age": age}
    response = supabase.table("pets").update(payload).match({"id": str(pet_id), "pet_owner": str(owner_id)}).execute()
    if response.error:
        raise Exception(f"Error updating pet: {response.error}")
    return response.data[0]

async def delete_pet(pet_id: UUID, owner_id: UUID):
    response = supabase.table("pets").delete().match({"id": str(pet_id), "pet_owner": str(owner_id)}).execute()
    return response.status_code == 204