from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from decimal import Decimal
from typing import List
from app.schemas.store import (
    ProductCreate, ProductOut,
    CartItemCreate, CartOut,
    OrderCreate, OrderOut
)
from app.services.supabase_store import (
    create_product, list_products,
    get_or_create_cart, add_to_cart,
    create_order
)
from app.auth.dependencies import get_current_user_id

router = APIRouter()

# Products
@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(
    payload: ProductCreate,
    user_id: UUID = Depends(get_current_user_id)
):
    # Only admin or receptionist
    from app.services.supabase_users import get_user_from_supabase
    current = await get_user_from_supabase(user_id)
    if current["role"] not in ("admin","recepcionista"):
        raise HTTPException(status_code=403, detail="Not authorized")
    data = payload.dict()
    return await create_product(data)

@router.get("/products", response_model=List[ProductOut])
async def list_products_endpoint():
    return await list_products()

# Cart
@router.get("/cart", response_model=CartOut)
async def get_cart_endpoint(
    user_id: UUID = Depends(get_current_user_id)
):
    cart = await get_or_create_cart(user_id)
    return cart

@router.post("/cart/items", response_model=None, status_code=status.HTTP_201_CREATED)
async def add_cart_item_endpoint(
    payload: CartItemCreate,
    user_id: UUID = Depends(get_current_user_id)
):
    cart = await get_or_create_cart(user_id)
    item = await add_to_cart(cart["id"], payload.product_id, payload.quantity)
    return item


@router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order_endpoint(
    payload: OrderCreate,
    user_id: UUID = Depends(get_current_user_id)
):
    from app.services.supabase_schedules import calculate_order_total  # assume a helper
    cart = await get_or_create_cart(user_id)
    items = []
    total = Decimal(0)
    for it in payload.items:
        
        prod = await supabase.table("products").select("price").eq("id", str(it.product_id)).single().execute()
        price = Decimal(prod.data[0]["price"])
        total += price * it.quantity
        items.append({
            "product_id": str(it.product_id),
            "quantity": it.quantity,
            "price": price
        })
    order_data = {
        "user_id": str(user_id),
        "status": "pending",
        "total_price": total
    }
    order = await create_order(order_data)
    
    for it in items:
        await supabase.table("order_items").insert({**it, "order_id": order["id"]}).execute()
    return {**order, "items": items}
