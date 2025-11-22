from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.order import OrderDetails, OrderItem

order_router = APIRouter(prefix="/order", tags=["order"])


class OrderItemIn(BaseModel):
    product_name: str
    product_id: int
    price: float
    quantity: int


class CheckoutRequest(BaseModel):
    user_id: int
    items: list[OrderItemIn]


@order_router.post("/checkout")
def checkout(data: CheckoutRequest, db: Session = Depends(get_db)):

    new_order_detail = OrderDetails(user_id=data.user_id)
    db.add(new_order_detail)
    db.flush()  # <-- generates new_order_detail.id before adding items

    total = 0

    # 2. Add order items
    for item in data.items:
        order_item = OrderItem(
            order_details_id=new_order_detail.id,
            product_name=item.product_name,
            product_id=item.product_id,
            price=item.price,
            quantity=item.quantity
        )
        db.add(order_item)
        total += item.price * item.quantity

    # 3. Update total price
    new_order_detail.total_price = total

    db.commit()
    db.refresh(new_order_detail)

    # 4. Return response
    return {
        "message": "Checkout saved successfully",
        "order_details_id": new_order_detail.id,
        "total": total,
        "items": [{"product_id": i.product_id, "product_name": i.product_name, "quantity": i.quantity, "price": i.price} for i in new_order_detail.items]
    }
