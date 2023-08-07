import uvicorn
from fastapi import FastAPI

from routers import User as UserRouter, UserCart as CartRouter, Product as ProductRouter

app = FastAPI()

app.include_router(UserRouter.router, prefix="/profile")
app.include_router(CartRouter.router, prefix="/profile/cart")
app.include_router(ProductRouter.router, prefix="/products")