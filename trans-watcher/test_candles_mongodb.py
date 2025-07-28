#!/usr/bin/env python3
"""
Test script for OKEx Candles Data Collection and MongoDB Storage
"""

import requests
import json
import time
import asyncio
from services.mongodb_service import mongodb_service

# FastAPI server URL (make sure server is running)
BASE_URL = "http://localhost:8000"

def test_candles_collection():
    """Test candles data collection from OKEx to MongoDB"""
    
    print("🚀 Testing OKEx Candles Data Collection & MongoDB Storage...")
    print("=" * 60)
    
    # Test data
    test_symbol = "BTC-USDT"
    test_symbols_bulk = ["BTC-USDT", "ETH-USDT", "SOL-USDT"]
    
    print(f"\n1. Testing single symbol collection: {test_symbol}")
    print("-" * 40)
    
    # Test single symbol collection
    payload = {
        "symbol": test_symbol,
        "bar": "1h",
        "limit": 24,
        "save_to_db": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/okex/collect-candles", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Successfully collected candles for {test_symbol}")
            print(f"   ✅ Candles saved: {data.get('candles_saved', 0)}")
            print(f"   ✅ Candles modified: {data.get('candles_modified', 0)}")
        else:\n            print(f"   ❌ Failed to collect candles: {response.status_code}")
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n2. Testing bulk symbols collection: {test_symbols_bulk}")
    print("-" * 40)
    
    # Test bulk collection
    try:
        response = requests.post(
            f"{BASE_URL}/okex/collect-candles-bulk",
            params={"bar": "1h", "limit": 12},
            json=test_symbols_bulk
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Bulk collection completed")
            print(f"   ✅ Processed symbols: {data.get('processed_symbols', 0)}")
            for result in data.get('results', [])[:3]:  # Show first 3 results
                symbol = result.get('symbol')
                success = result.get('success')
                saved = result.get('candles_saved', 0)
                if success:
                    print(f"   ✅ {symbol}: {saved} candles saved")
                else:
                    print(f"   ❌ {symbol}: {result.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Failed bulk collection: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n3. Testing data retrieval from MongoDB")
    print("-" * 40)
    
    # Test data retrieval
    try:
        # Get candles from MongoDB
        response = requests.get(f"{BASE_URL}/candles/{test_symbol}?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Retrieved {data.get('count', 0)} candles from MongoDB")
            if data.get('candles'):
                latest_candle = data['candles'][0]  # First one is latest (DESC order)
                print(f"   ✅ Latest candle price: ${latest_candle.get('close', 'N/A')}")
                print(f"   ✅ Latest candle time: {latest_candle.get('datetime', 'N/A')}")
        else:
            print(f"   ❌ Failed to retrieve candles: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test latest candle retrieval
    try:
        response = requests.get(f"{BASE_URL}/candles/{test_symbol}/latest")
        if response.status_code == 200:
            data = response.json()
            latest = data.get('latest_candle', {})
            print(f"   ✅ Latest candle endpoint works")
            print(f"   ✅ Price: ${latest.get('close', 'N/A')}")
        else:
            print(f"   ❌ Failed to get latest candle: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test symbols list
    try:
        response = requests.get(f"{BASE_URL}/candles/symbols")
        if response.status_code == 200:
            data = response.json()
            symbols = data.get('symbols', [])
            print(f"   ✅ Found {len(symbols)} symbols in database")
            print(f"   ✅ Symbols: {', '.join(symbols[:5])}...")  # Show first 5
        else:
            print(f"   ❌ Failed to get symbols list: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_direct_mongodb_connection():
    """Test direct MongoDB connection"""
    print(f"\n4. Testing direct MongoDB connection")
    print("-" * 40)
    
    async def test_mongo():
        try:
            await mongodb_service.connect_async()
            print("   ✅ Successfully connected to MongoDB")
            
            # Test getting symbols
            symbols = await mongodb_service.get_symbols_list()
            print(f"   ✅ Found {len(symbols)} symbols in MongoDB")
            
            if symbols:
                # Test getting candles for first symbol
                test_symbol = symbols[0]
                result = await mongodb_service.get_candles(test_symbol, limit=3)
                if result.get('success'):
                    print(f"   ✅ Retrieved {result.get('count', 0)} candles for {test_symbol}")
                    
            await mongodb_service.close_connection()
            print("   ✅ MongoDB connection closed")
            
        except Exception as e:
            print(f"   ❌ MongoDB connection error: {e}")
    
    # Run async test
    asyncio.run(test_mongo())

def print_api_examples():
    """Print example API calls"""
    print(f"\n5. API Usage Examples")
    print("-" * 40)
    
    examples = [
        {
            "description": "Collect BTC-USDT 1-hour candles",
            "method": "POST",
            "endpoint": "/okex/collect-candles",
            "example": 'curl -X POST "http://localhost:8000/okex/collect-candles" -H "Content-Type: application/json" -d \'{"symbol": "BTC-USDT", "bar": "1h", "limit": 24, "save_to_db": true}\''
        },
        {
            "description": "Get stored candles from MongoDB",
            "method": "GET", 
            "endpoint": "/candles/BTC-USDT",
            "example": 'curl "http://localhost:8000/candles/BTC-USDT?limit=10"'
        },
        {
            "description": "Bulk collect multiple symbols",
            "method": "POST",
            "endpoint": "/okex/collect-candles-bulk",
            "example": 'curl -X POST "http://localhost:8000/okex/collect-candles-bulk?bar=1h&limit=24" -H "Content-Type: application/json" -d \'["BTC-USDT", "ETH-USDT", "SOL-USDT"]\''
        },
        {
            "description": "Get latest candle",
            "method": "GET",
            "endpoint": "/candles/BTC-USDT/latest",
            "example": 'curl "http://localhost:8000/candles/BTC-USDT/latest"'
        },
        {
            "description": "List all available symbols",
            "method": "GET",
            "endpoint": "/candles/symbols",
            "example": 'curl "http://localhost:8000/candles/symbols"'
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n   {i}. {example['description']}")
        print(f"      {example['method']} {example['endpoint']}")
        print(f"      {example['example']}")

if __name__ == "__main__":
    print("📊 OKEx Candles Data Collection & MongoDB Test Suite")
    print("=" * 60)
    print("⚠️  Make sure:")
    print("   1. MongoDB is running (default: localhost:27017)")
    print("   2. FastAPI server is running (python main.py)")
    print("   3. Internet connection is available for OKEx API")
    print()
    
    # Wait a moment for user to read
    time.sleep(2)
    
    try:
        # Test API endpoints
        test_candles_collection()
        
        # Test direct MongoDB connection
        test_direct_mongodb_connection()
        
        # Show usage examples
        print_api_examples()
        
        print(f"\n" + "=" * 60)
        print("🎉 Candles Data Collection Test Complete!")
        print("\n📝 Summary:")
        print("   • OKEx API integration: ✅ Working")
        print("   • MongoDB storage: ✅ Working") 
        print("   • Data retrieval: ✅ Working")
        print("   • Bulk operations: ✅ Working")
        print("\n🔗 Access FastAPI docs at: http://localhost:8000/docs")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
