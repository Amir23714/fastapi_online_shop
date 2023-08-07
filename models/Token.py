from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="token")
