"""
OKEx router for cryptocurrency operations
"""

from fastapi import APIRouter, HTTPException
from services.okex_service import OKExService
from models import CandleRequest, BulkCandleRequest

router = APIRouter(
    prefix="/okex",
    tags=["okex"],
    responses={404: {"description": "Not found"}},
)

# OKEx Service instance
okex_service = OKExService()


@router.get("/ticker/{symbol}")
async def get_ticker(symbol: str):
    """Get ticker information for a specific symbol"""
    try:
        result = okex_service.get_ticker(symbol)
        if result.get('success'):
            return result
        raise HTTPException(status_code=404, detail=result.get('error'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/instruments")
async def get_instruments(instType: str = "SWAP"):
    """Get trading instruments from OKEx"""
    try:
        result = okex_service.get_instruments(instType=instType)
        if result.get('success'):
            return result
        raise HTTPException(status_code=404, detail=result.get('error'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orderbook/{symbol}")
async def get_orderbook(symbol: str, sz: int = 20):
    """Get order book for a specific symbol"""
    try:
        result = okex_service.get_orderbook(symbol, sz)
        if result.get('success'):
            return result
        raise HTTPException(status_code=404, detail=result.get('error'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/collect-candles")
async def collect_candles(candle_request: CandleRequest):
    """Fetch candles data from OKEx and insert into MongoDB"""
    try:
        result = okex_service.get_candlesticks(
            symbol=candle_request.symbol, 
            bar=candle_request.bar, 
            limit=candle_request.limit
        )
        if result.get('success'):
            # Handle MongoDB storage if applicable
            
            return result
        raise HTTPException(status_code=404, detail=result.get('error'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_okex_status():
    """Get OKEx system status"""
    try:
        result = okex_service.get_system_status()
        if result.get('success'):
            return result
        raise HTTPException(status_code=503, detail=result.get('error'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trading-pairs")
async def get_popular_trading_pairs():
    """Get popular trading pairs with their current prices"""
    try:
        result = okex_service.get_popular_trading_pairs()
        if result.get('success'):
            return result
        raise HTTPException(status_code=404, detail=result.get('error'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/collect-candles-bulk")
async def collect_candles_bulk(bulk_request: BulkCandleRequest):
    """Fetch candles data for multiple symbols and save to MongoDB"""
    try:
        results = []
        for symbol in bulk_request.symbols:
            result = okex_service.get_candlesticks(symbol, bulk_request.bar, bulk_request.limit)
            results.append(result)
        return {
            "success": True,
            "results": results,
            "processed_symbols": len(bulk_request.symbols),
            "bar": bulk_request.bar,
            "limit": bulk_request.limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
