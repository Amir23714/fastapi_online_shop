import uvicorn
from fastapi import FastAPI
from routers import User as UserRouter, UserCart as CartRouter, Product as ProductRouter

app = FastAPI()

app.include_router(UserRouter.router, prefix="/api/profile")
app.include_router(CartRouter.router, prefix="/api/profile/cart")
app.include_router(ProductRouter.router, prefix="/api/products")

# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses = True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi_cache")