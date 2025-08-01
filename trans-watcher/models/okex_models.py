"""
OKEx API models for cryptocurrency data
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class OKXConfig(BaseModel):
    """Configuration model for OKEx API credentials"""
    api_key: str
    secret_key: str
    passphrase: str
    flag: str = Field(default="0", description="0: Production, 1: Sandbox")


class TickerResponse(BaseModel):
    """Model for OKEx ticker response"""
    instId: str = Field(description="Instrument ID")
    last: str = Field(description="Last traded price")
    lastSz: str = Field(description="Last traded size")
    askPx: str = Field(description="Best ask price")
    askSz: str = Field(description="Best ask size")
    bidPx: str = Field(description="Best bid price")
    bidSz: str = Field(description="Best bid size")
    open24h: str = Field(description="24h opening price")
    high24h: str = Field(description="24h highest price")
    low24h: str = Field(description="24h lowest price")
    volCcy24h: str = Field(description="24h volume in quote currency")
    vol24h: str = Field(description="24h volume in base currency")
    ts: str = Field(description="Timestamp")
    sodUtc0: str = Field(description="Start of day UTC+0")
    sodUtc8: str = Field(description="Start of day UTC+8")


class CandleRequest(BaseModel):
    """Model for requesting candle data"""
    symbol: str = Field(description="Trading pair symbol (e.g., BTC-USDT)")
    bar: str = Field(
        default="1h", 
        description="Time frame: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d, 1w, 1M, 3M"
    )
    limit: int = Field(default=100, ge=1, le=300, description="Number of candles to fetch (1-300)")


class CandleResponse(BaseModel):
    """Model for candle data response"""
    timestamp: int = Field(description="Timestamp in milliseconds")
    datetime: str = Field(description="Human readable datetime")
    open: float = Field(description="Opening price")
    high: float = Field(description="Highest price")
    low: float = Field(description="Lowest price")
    close: float = Field(description="Closing price")
    volume: float = Field(description="Trading volume")


class TradingPair(BaseModel):
    """Model for trading pair information"""
    symbol: str = Field(description="Trading pair symbol")
    price: str = Field(description="Current price")
    change_24h: str = Field(description="24h price change")
    volume_24h: str = Field(description="24h trading volume")
    high_24h: str = Field(description="24h highest price")
    low_24h: str = Field(description="24h lowest price")


class BulkCandleRequest(BaseModel):
    """Model for bulk candle data collection"""
    symbols: List[str] = Field(description="List of trading pair symbols")
    bar: str = Field(default="1h", description="Time frame")
    limit: int = Field(default=100, ge=1, le=300, description="Number of candles per symbol")


class CandleCollectionResult(BaseModel):
    """Model for candle collection operation result"""
    symbol: str = Field(description="Trading pair symbol")
    success: bool = Field(description="Whether the operation was successful")
    candles_saved: Optional[int] = Field(default=None, description="Number of candles saved")
    candles_modified: Optional[int] = Field(default=None, description="Number of candles modified")
    error: Optional[str] = Field(default=None, description="Error message if operation failed")


class BulkCandleResponse(BaseModel):
    """Model for bulk candle collection response"""
    success: bool = Field(description="Overall operation success")
    results: List[CandleCollectionResult] = Field(description="Individual symbol results")
    processed_symbols: int = Field(description="Number of symbols processed")
    bar: str = Field(description="Time frame used")
    limit: int = Field(description="Limit used per symbol")


class CandleQueryResponse(BaseModel):
    """Model for candle query response from MongoDB"""
    success: bool = Field(description="Query success status")
    symbol: str = Field(description="Trading pair symbol")
    count: int = Field(description="Number of candles returned")
    candles: List[CandleResponse] = Field(description="List of candle data")


class SymbolsListResponse(BaseModel):
    """Model for symbols list response"""
    success: bool = Field(description="Query success status")
    symbols: List[str] = Field(description="List of available symbols")
    count: int = Field(description="Number of symbols")


class LatestCandleResponse(BaseModel):
    """Model for latest candle response"""
    success: bool = Field(description="Query success status")
    symbol: str = Field(description="Trading pair symbol")
    latest_candle: CandleResponse = Field(description="Latest candle data")


class APIResponse(BaseModel):
    """Generic API response model"""
    success: bool = Field(description="Operation success status")
    message: Optional[str] = Field(default=None, description="Response message")
    data: Optional[dict] = Field(default=None, description="Response data")
    timestamp: Optional[str] = Field(default=None, description="Response timestamp")


class HealthCheckResponse(BaseModel):
    """Model for health check response"""
    status: str = Field(description="Service status")
    service: str = Field(description="Service name")
    timestamp: Optional[str] = Field(default=None, description="Check timestamp")


class OKExStatusResponse(BaseModel):
    """Model for OKEx API status response"""
    success: bool = Field(description="Connection success status")
    okex_time: str = Field(description="OKEx server timestamp")
    local_time: str = Field(description="Local server timestamp")
    status: str = Field(description="Connection status message")
