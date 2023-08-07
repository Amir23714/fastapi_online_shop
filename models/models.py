from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

ALCHEMY_URL = "sqlite:///gg_db.db"

engine = create_engine(ALCHEMY_URL)

SessonLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    with SessonLocal() as session:
        yield session


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, index = True)

    isLoggedIn = Column(Boolean, index=True, default=False)

    isAdmin = Column(Boolean, index = True, default=False)

    cart_id = Column(Integer, index=True)

class UserCart(Base):
    __tablename__ = "usercarts"

    id = Column(Integer, primary_key=True, index=True)
    items = Column(String, index=True)
    total_price = Column(Integer, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount = Column(Integer, index=True)
    description = Column(String, index=True)
    price = Column(Integer, index=True)

    isVisible = Column(Boolean, index=True)

