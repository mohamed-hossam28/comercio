from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.cart import Cart, CartItem

cart_router = APIRouter(prefix="/cart", tags=["Cart"])

class CartItemIn(BaseModel):
    product_name: str
    price: float
    quantity: int

class CheckoutRequest(BaseModel):
    user_id: int
    items: list[CartItemIn]

@cart_router.post("/checkout")
def checkout_cart(data: CheckoutRequest, db: Session = Depends(get_db)):
  
    new_cart = Cart(user_id=data.user_id)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    total = 0

  
    for item in data.items:
        cart_item = CartItem(
            cart_id=new_cart.id,
            product_name=item.product_name,
            price=item.price,
            quantity=item.quantity
        )
        total += item.price * item.quantity
        db.add(cart_item)

    new_cart.total_price = total
    db.commit()

    return {
        "message": "Checkout saved successfully",
        "cart_id": new_cart.id,
        "total": total
    }