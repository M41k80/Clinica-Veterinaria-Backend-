import os
from supabase import create_client, Client
from uuid import UUID
from decimal import Decimal
from typing import List

SUPABASE_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Products
async def create_product(data: dict) -> dict:
    res = supabase.table("products").insert(data).execute()
    if res.status_code != 201:
        raise Exception(res.error)
    return res.data[0]

async def list_products() -> List[dict]:
    res = supabase.table("products").select("*").execute()
    return res.data

# Carts
async def get_or_create_cart(user_id: UUID) -> dict:
    res = supabase.table("carts").select("*").eq("user_id", str(user_id)).single().execute()
    if res.status_code == 406 or res.data is None:
        res = supabase.table("carts").insert({"user_id": str(user_id)}).execute()
    return res.data

async def add_to_cart(cart_id: UUID, product_id: UUID, quantity: int) -> dict:
    data = {"cart_id": str(cart_id), "product_id": str(product_id), "quantity": quantity}
    res = supabase.table("cart_items").insert(data).execute()
    return res.data[0]

# Orders
async def create_order(data: dict) -> dict:
    res = supabase.table("orders").insert(data).execute()
    if res.status_code != 201:
        raise Exception(res.error)
    order = res.data[0]
    return order