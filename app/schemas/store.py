from pydantic import BaseModel, Field, condecimal
from uuid import UUID
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Product price")
    stock: int = Field(..., ge=0, description="Stock quantity")
    category: str = Field(..., description="Product category: food, medicine, accessory, other")
    image_url: Optional[str] = Field(None, description="URL of product image")

class ProductOut(ProductCreate):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}

class CartItemCreate(BaseModel):
    product_id: UUID = Field(..., description="UUID of product")
    quantity: int = Field(..., ge=1, description="Quantity to add")

class CartItemOut(CartItemCreate):
    id: UUID

class CartOut(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    items: List[CartItemOut]

    model_config = {"from_attributes": True}

class OrderCreate(BaseModel):
    items: List[CartItemCreate] = Field(..., description="Items in the order")

class OrderOut(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    status: str
    total_price: condecimal(max_digits=10, decimal_places=2)
    items: List[CartItemOut]

    model_config = {"from_attributes": True}