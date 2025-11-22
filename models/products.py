from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Product(Base):
    tablename = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    image = Column(String(255), nullable=False) 
    category = Column(String(50), nullable=False)
    stock = Column(Integer, default=0)