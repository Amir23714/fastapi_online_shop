from typing import Optional

from pydantic import BaseModel


class ProductUpdate(BaseModel):
    id : int
    amount: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
    isVisible: Optional[bool] = None
