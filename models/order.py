from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class OrderDetails(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float, default=0)

    # One order has many items
    items = relationship("OrderItem", back_populates="order_details")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_details_id = Column(Integer, ForeignKey("order_details.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    # Each item belongs to one OrderDetails
    order_details = relationship("OrderDetails", back_populates="items")
