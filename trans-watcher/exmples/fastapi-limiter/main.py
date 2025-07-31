from contextlib import asynccontextmanager

import redis.asyncio as redis
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Response, WebSocket

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter, WebSocketRateLimiter
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)


async def fallback_to_index(request: Request, response: Response, pexpire: int):
    raise HTTPException(
        430, "Too Many Requests", headers={}
    )

@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5, callback=fallback_to_index))])
async def index_get():
    return {"msg": "Hello World"}

@app.post("/", dependencies=[Depends(RateLimiter(times=1, seconds=5))])
async def index_post():
    return {"msg": "Hello World"}


@app.get(
    "/multiple",
    dependencies=[
        Depends(RateLimiter(times=1, seconds=5)),
        Depends(RateLimiter(times=2, seconds=15)),
    ],
)
async def multiple():
    return {"msg": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ratelimit = WebSocketRateLimiter(times=1, seconds=5)
    while True:
        try:
            data = await websocket.receive_text()
            await ratelimit(websocket, context_key=data)  # NB: context_key is optional
            await websocket.send_text("Hello, world")
        except HTTPException:
            await websocket.send_text("Hello again")
            
@app.exception_handler(430)
async def rate_limit_exceeded(request: Request, exc):
    return JSONResponse(
        status_code=200,
        content={"msg": "请求过快"}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)