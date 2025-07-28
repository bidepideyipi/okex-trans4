"""
Candles router for MongoDB operations
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, List
from services.mongodb_service import mongodb_service
from models import CandleRequest

router = APIRouter(
    prefix="/candles",
    tags=["candles"],
    responses={404: {"description": "Not found"}},
)

# Use the global mongodb_service instance


@router.get("/{symbol}")
async def get_candles_from_db(
    symbol: str, 
    limit: int = 100, 
    start_time: Optional[str] = None, 
    end_time: Optional[str] = None
):
    """Get candles data from MongoDB"""
    try:
        # Convert string timestamps to integers if provided
        start_ts = int(start_time) if start_time else None
        end_ts = int(end_time) if end_time else None
        
        result = await mongodb_service.get_candles(symbol, limit, start_ts, end_ts)
        
        if result.get('success'):
            return result
        else:
            raise HTTPException(status_code=404, detail=result.get('error', 'Candles data not found'))
            
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving candles data: {str(e)}")


@router.get("/{symbol}/latest")
async def get_latest_candle_from_db(symbol: str):
    """Get the latest candle for a symbol from MongoDB"""
    try:
        result = await mongodb_service.get_latest_candle(symbol)
        
        if result:
            return {
                "success": True,
                "symbol": symbol,
                "latest_candle": result
            }
        else:
            raise HTTPException(status_code=404, detail=f"No candles found for {symbol}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving latest candle: {str(e)}")


@router.get("/symbols/")
async def get_available_symbols():
    """Get list of all symbols available in the database"""
    try:
        symbols = await mongodb_service.get_symbols_list()
        return {
            "success": True,
            "symbols": symbols,
            "count": len(symbols)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving symbols: {str(e)}")


@router.post("/collect/{symbol}")
async def collect_and_store_candles(symbol: str, candle_request: CandleRequest):
    """Collect candles from OKEx and store in MongoDB"""
    try:
        # This will be implemented to integrate with OKEx service
        # and store the data using MongoDB service
        return {
            "success": True,
            "message": f"Collection endpoint for {symbol} - to be implemented"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
