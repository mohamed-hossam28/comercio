
from fastapi import APIRouter, Depends, HTTPException, status
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

class PurchaseRequest(BaseModel):
    quantity: int

@products_router.get("/products/grouped", response_model=Dict[str, List[ProductSchema]])
def get_products(db: Session = Depends(get_db), limit: int = 20):
    products = db.query(Product).all()
    grouped_data = defaultdict(list)
    for product in products:
        category = product.category.capitalize() if product.category else "Other"
        if len(grouped_data[category]) < limit:
            grouped_data[category].append(product)

    return grouped_data

@products_router.post("/products/{product_id}/purchase", status_code=status.HTTP_200_OK)
def purchase_product(product_id: int, request: PurchaseRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock_avilabilty < request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    product.stock_avilabilty -= request.quantity
    db.commit()
    db.refresh(product)
    
    return {"message": "Purchase successful", "new_stock": product.stock_avilabilty}


@products_router.get("/products/search", response_model=List[ProductSchema])
def search_products(q: str, db: Session = Depends(get_db)):
    if not q:
        return []
    products = db.query(Product).filter(Product.name.ilike(f"%{q}%")).all()
    return products
