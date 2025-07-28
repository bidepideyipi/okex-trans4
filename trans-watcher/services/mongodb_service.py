#!/usr/bin/env python3
"""
MongoDB Manager for OKEx Candles Data
Handles connection to MongoDB and CRUD operations for candles data
"""

import motor.motor_asyncio
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timezone
from typing import List, Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBService:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", database_name: str = "okex_data"):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection string
            database_name: Database name to use
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.async_client = None
        self.db = None
        self.async_db = None
        
    async def connect_async(self):
        """Establish async MongoDB connection"""
        try:
            self.async_client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string)
            self.async_db = self.async_client[self.database_name]
            
            # Test connection
            await self.async_client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB (async): {self.database_name}")
            
            # Create indexes for better performance
            await self.create_indexes()
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB (async): {e}")
            raise
    
    def connect_sync(self):
        """Establish sync MongoDB connection"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.database_name]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB (sync): {self.database_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB (sync): {e}")
            raise
    
    async def create_indexes(self):
        """Create indexes for candles collections"""
        try:
            collections_to_index = ["candles"]
            
            for collection_name in collections_to_index:
                collection = self.async_db[collection_name]
                
                # Create compound index on symbol and timestamp for efficient queries
                await collection.create_index([
                    ("symbol", ASCENDING),
                    ("timestamp", ASCENDING)
                ], unique=True)
                
                # Create index on timestamp for time-based queries
                await collection.create_index([("timestamp", DESCENDING)])
                
                # Create index on symbol for symbol-based queries
                await collection.create_index([("symbol", ASCENDING)])
                
            logger.info("Successfully created indexes")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    async def insert_candles(self, symbol: str, candles_data: List[Dict]) -> Dict:
        """
        Insert candles data into MongoDB
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC-USDT')
            candles_data: List of candle data dictionaries
            
        Returns:
            Dictionary with insertion results
        """
        try:
            if not self.async_db:
                await self.connect_async()
            
            collection = self.async_db["candles"]
            
            # Process and format candles data
            processed_candles = []
            for candle in candles_data:
                # OKEx candle format: [timestamp, open, high, low, close, volume, volCcy, volCcyQuote, confirm]
                processed_candle = {
                    "symbol": symbol,
                    "timestamp": int(candle[0]),  # Timestamp in milliseconds
                    "datetime": datetime.fromtimestamp(int(candle[0]) / 1000, tz=timezone.utc),
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5]),
                    "volume_currency": float(candle[6]) if candle[6] else 0.0,
                    "volume_currency_quote": float(candle[7]) if candle[7] else 0.0,
                    "confirmed": int(candle[8]) if len(candle) > 8 else 1,
                    "inserted_at": datetime.now(tz=timezone.utc)
                }
                processed_candles.append(processed_candle)
            
            # Use upsert to handle duplicates
            operations = []
            for candle in processed_candles:
                operations.append({
                    "replaceOne": {
                        "filter": {
                            "symbol": candle["symbol"],
                            "timestamp": candle["timestamp"]
                        },
                        "replacement": candle,
                        "upsert": True
                    }
                })
            
            if operations:
                result = await collection.bulk_write(operations)
                
                return {
                    "success": True,
                    "symbol": symbol,
                    "total_candles": len(candles_data),
                    "inserted_count": result.upserted_count,
                    "modified_count": result.modified_count,
                    "matched_count": result.matched_count,
                    "timestamp": datetime.now(tz=timezone.utc).isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": "No candles data to insert"
                }
                
        except Exception as e:
            logger.error(f"Error inserting candles data: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_candles(self, symbol: str, limit: int = 100, start_time: Optional[int] = None, end_time: Optional[int] = None) -> Dict:
        """
        Retrieve candles data from MongoDB
        
        Args:
            symbol: Trading pair symbol
            limit: Maximum number of candles to return
            start_time: Start timestamp (milliseconds)
            end_time: End timestamp (milliseconds)
            
        Returns:
            Dictionary with candles data
        """
        try:
            if not self.async_db:
                await self.connect_async()
            
            collection = self.async_db["candles"]
            
            # Build query filter
            query_filter = {"symbol": symbol}
            
            if start_time or end_time:
                timestamp_filter = {}
                if start_time:
                    timestamp_filter["$gte"] = start_time
                if end_time:
                    timestamp_filter["$lte"] = end_time
                query_filter["timestamp"] = timestamp_filter
            
            # Execute query
            cursor = collection.find(query_filter).sort("timestamp", DESCENDING).limit(limit)
            candles = await cursor.to_list(length=limit)
            
            # Format response
            formatted_candles = []
            for candle in candles:
                formatted_candles.append({
                    "timestamp": candle["timestamp"],
                    "datetime": candle["datetime"].isoformat(),
                    "open": candle["open"],
                    "high": candle["high"],
                    "low": candle["low"],
                    "close": candle["close"],
                    "volume": candle["volume"]
                })
            
            return {
                "success": True,
                "symbol": symbol,
                "count": len(formatted_candles),
                "candles": formatted_candles
            }
            
        except Exception as e:
            logger.error(f"Error retrieving candles data: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_symbols_list(self) -> List[str]:
        """Get list of all symbols in the database"""
        try:
            if not self.async_db:
                await self.connect_async()
            
            collection = self.async_db["candles"]
            symbols = await collection.distinct("symbol")
            return symbols
            
        except Exception as e:
            logger.error(f"Error getting symbols list: {e}")
            return []
    
    async def get_latest_candle(self, symbol: str) -> Optional[Dict]:
        """Get the latest candle for a symbol"""
        try:
            if not self.async_db:
                await self.connect_async()
            
            collection = self.async_db["candles"]
            latest_candle = await collection.find_one(
                {"symbol": symbol},
                sort=[("timestamp", DESCENDING)]
            )
            
            if latest_candle:
                return {
                    "timestamp": latest_candle["timestamp"],
                    "datetime": latest_candle["datetime"].isoformat(),
                    "open": latest_candle["open"],
                    "high": latest_candle["high"],
                    "low": latest_candle["low"],
                    "close": latest_candle["close"],
                    "volume": latest_candle["volume"]
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting latest candle: {e}")
            return None
    
    async def close_connection(self):
        """Close MongoDB connections"""
        if self.async_client:
            self.async_client.close()
        if self.client:
            self.client.close()
        logger.info("MongoDB connections closed")

# Global MongoDB service instance
mongodb_service = MongoDBService()
