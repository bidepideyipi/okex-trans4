# 新位置: core/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis

@asynccontextmanager
async def app_lifespan(_: FastAPI):
    # 应用启动时初始化
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    
    # 应用运行期间保持连接
    yield
    
    # 应用关闭时释放资源
    await FastAPILimiter.close()

