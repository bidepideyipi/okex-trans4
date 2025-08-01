"""
FastAPI Demo with OKEx Integration and MongoDB Storage
Main application file using organized structure with routers, services, and models
"""

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimiter
import uvicorn
from datetime import datetime
from routers import items_router, okex_router, candles_router
from models.okex_models import HealthCheckResponse
from middleware import app_lifespan


# Create FastAPI instance
app = FastAPI(
    title="FastAPI Demo with OKEx Integration",
    description="A FastAPI demonstration with OKEx cryptocurrency API and MongoDB integration",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=app_lifespan 
)

# Include routers
app.include_router(items_router)
app.include_router(okex_router)  
app.include_router(candles_router)

# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint with basic information"""
    return {
        "message": "Welcome to FastAPI Demo with OKEx Integration!",
        "version": "2.0.0",
        "features": [
            "Basic CRUD operations",
            "OKEx cryptocurrency API integration", 
            "MongoDB candles data storage",
            "Real-time market data"
        ],
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        service="FastAPI Demo with OKEx Integration",
        timestamp=datetime.now().isoformat()
    )

async def fallback_to_info(request: Request, response: Response, pexpire: int):
    raise HTTPException(
        430, "Too Many Requests", headers={}
    )
    
@app.exception_handler(430)
async def rate_limit_exceeded(request: Request, exc):
    return JSONResponse(
        status_code=200,
        content={"msg": "请求过快"}
    )
    
# Additional info endpoint
@app.get("/info", dependencies=[Depends(RateLimiter(times=2, seconds=5, callback=fallback_to_info))])
async def get_api_info():
    """Get API information and available endpoints"""
    return {
        "name": "FastAPI Demo with OKEx Integration",
        "version": "2.0.0",
        "description": "A demonstration of FastAPI with cryptocurrency data integration",
        "endpoints": {
            "items": {
                "description": "Basic CRUD operations",
                "base_path": "/items"
            },
            "okex": {
                "description": "OKEx cryptocurrency API integration",
                "base_path": "/okex"
            },
            "candles": {
                "description": "MongoDB candles data operations",
                "base_path": "/candles"
            }
        },
        "technologies": [
            "FastAPI",
            "Pydantic",
            "OKEx SDK",
            "MongoDB",
            "Motor (async MongoDB driver)"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
