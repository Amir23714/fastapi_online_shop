from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, index = True)

    isLoggedIn = Column(Boolean, index=True, default=False)

    isAdmin = Column(Boolean, index = True, default=False)


    cart = relationship("UserCart", back_populates="user", uselist=False)