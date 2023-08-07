from sqlalchemy import Boolean, Column, Integer, String

from database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount = Column(Integer, index=True)
    description = Column(String, index=True)
    price = Column(Integer, index=True)

    isVisible = Column(Boolean, index=True)