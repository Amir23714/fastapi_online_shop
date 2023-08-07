from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class UserCart(Base):
    __tablename__ = "usercarts"

    id = Column(Integer, primary_key=True, index=True)
    items = Column(String, index=True)
    total_price = Column(Integer, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="cart")