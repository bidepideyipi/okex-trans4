"""
OKEx API service for handling cryptocurrency data operations
"""

import okx.MarketData as MarketData
import okx.PublicData as PublicData
from typing import Dict, List, Optional
from datetime import datetime


class OKExService:
    """Service class for OKEx API operations"""
    
    def __init__(self, api_key: str = "", api_secret_key: str = "", passphrase: str = "", flag: str = "0"):
        """
        Initialize OKEx service
        
        Args:
            api_key: OKEx API key (empty for public endpoints)
            api_secret_key: OKEx API secret key (empty for public endpoints)
            passphrase: OKEx API passphrase (empty for public endpoints)
            flag: Environment flag (0: Production, 1: Sandbox)
        """
        self.market_api = MarketData.MarketAPI(
            api_key=api_key,
            api_secret_key=api_secret_key,
            passphrase=passphrase,
            use_server_time=False,
            flag=flag
        )
        
        self.public_api = PublicData.PublicAPI(
            api_key=api_key,
            api_secret_key=api_secret_key,
            passphrase=passphrase,
            use_server_time=False,
            flag=flag
        )
    
    def get_ticker(self, symbol: str) -> Dict:
        """Get ticker information for a symbol"""
        try:
            result = self.market_api.get_ticker(instId=symbol)
            if result and result.get('code') == '0' and result.get('data'):
                return {
                    "success": True,
                    "data": result['data'][0],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Ticker data not found for {symbol}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_instruments(self, instType: str = "SWAP") -> Dict:
        """Get trading instruments"""
        try:
            result = self.public_api.get_instruments(instType=instType)
            if result and result.get('code') == '0':
                return {
                    "success": True,
                    "data": result['data'][:10],  # Limit to first 10 for demo
                    "total_count": len(result['data']),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": "Instruments data not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_orderbook(self, symbol: str, size: int = 20) -> Dict:
        """Get order book for a symbol"""
        try:
            result = self.market_api.get_orderbook(instId=symbol, sz=str(size))
            if result and result.get('code') == '0' and result.get('data'):
                return {
                    "success": True,
                    "data": result['data'][0],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Order book data not found for {symbol}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_candlesticks(self, symbol: str, bar: str = "1m", limit: int = 100) -> Dict:
        """Get candlestick data for a symbol"""
        try:
            result = self.market_api.get_candlesticks(instId=symbol, bar=bar, limit=str(limit))
            if result and result.get('code') == '0' and result.get('data'):
                return {
                    "success": True,
                    "data": result['data'],
                    "symbol": symbol,
                    "bar": bar,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"Candlestick data not found for {symbol}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_system_status(self) -> Dict:
        """Get OKEx system status"""
        try:
            result = self.public_api.get_system_time()
            if result and result.get('code') == '0':
                return {
                    "success": True,
                    "okex_time": result['data'][0]['ts'],
                    "local_time": datetime.now().isoformat(),
                    "status": "Connected to OKEx API"
                }
            else:
                return {
                    "success": False,
                    "error": "Unable to connect to OKEx API"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_popular_trading_pairs(self) -> Dict:
        """Get popular trading pairs with their current prices"""
        try:
            popular_pairs = ["BTC-USDT", "ETH-USDT", "BNB-USDT", "ADA-USDT", "SOL-USDT"]
            results = []
            
            for pair in popular_pairs:
                try:
                    ticker_result = self.market_api.get_ticker(instId=pair)
                    if ticker_result and ticker_result.get('code') == '0' and ticker_result.get('data'):
                        data = ticker_result['data'][0]
                        results.append({
                            "symbol": pair,
                            "price": data.get('last', 'N/A'),
                            "change_24h": data.get('open24h', 'N/A'),
                            "volume_24h": data.get('vol24h', 'N/A'),
                            "high_24h": data.get('high24h', 'N/A'),
                            "low_24h": data.get('low24h', 'N/A')
                        })
                except:
                    continue
            
            return {
                "success": True,
                "data": results,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
