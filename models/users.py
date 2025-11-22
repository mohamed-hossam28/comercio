from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(String)
    email = Column(String)
    password = Column(String)
    sex = Column(String)
    phone = Column(String)
    country = Column(String)
