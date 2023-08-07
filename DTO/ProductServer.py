from typing import Optional

from pydantic import BaseModel


class ProductServer(BaseModel):
    id: int
    amount: int = None
