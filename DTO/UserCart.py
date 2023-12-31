from pydantic import BaseModel


class UserCart(BaseModel):
    items: str
    total_price: str
    user_id : int
