from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from typing import Dict, List
from models.products import Product
from collections import defaultdict

products_router = APIRouter()

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    image_url: str
    category: str
    description: str | None = None
    stock_avilabilty: int

    class Config:
        from_attributes = True

@products_router.get("/products/grouped", response_model=Dict[str, List[ProductSchema]])
def get_products(db: Session = Depends(get_db), limit: int = 4):
    products = db.query(Product).all()
    grouped_data = defaultdict(list)
    for product in products:
        category = product.category.capitalize() if product.category else "Other"
        if len(grouped_data[category]) < limit:
            grouped_data[category].append(product)

    return grouped_data

