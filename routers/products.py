from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from typing import Dict, List
from models import products

order_router = APIRouter()

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    image_url: str
    category: str

    class Config:
        from_attributes = True

@order_router.get("/products/grouped", response_model=Dict[str, List[ProductSchema]])
def get_products(db: Session = Depends(get_db),limit: int = 4):
    products = db.query(products).all()
    grouped_data = defaultdict(list)
    for product in products:
        if len(grouped_data[product.category]) < limit:
            grouped_data[product.category].append(product)

    return grouped_data

