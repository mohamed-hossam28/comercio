from sqlalchemy import Column, Integer, String, Float, Text
from database import Base


class Product(Base):
	__tablename__ = "products"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True, nullable=False)
	description = Column(Text)
	price = Column(Float, nullable=False)

