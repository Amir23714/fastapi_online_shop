import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from routers import User as UserRouter, UserCart as CartRouter, Product as ProductRouter

app = FastAPI()

app.include_router(UserRouter.router, prefix="/profile")
app.include_router(CartRouter.router, prefix="/profile/cart")
app.include_router(ProductRouter.router, prefix="/products")


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses = True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi_cache")