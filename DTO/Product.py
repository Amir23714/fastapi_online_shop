from pydantic import BaseModel


class Product(BaseModel):
    name: str
    amount: int
    description: str
    price: int
    isVisible: bool
