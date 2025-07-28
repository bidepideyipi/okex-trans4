#!/usr/bin/env python3
"""
Test script to verify OKEx API integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import okx.MarketData as MarketData
import okx.PublicData as PublicData
from datetime import datetime

def test_okex_integration():
    """Test basic OKEx API functionality"""
    
    # Initialize API clients (no credentials needed for public endpoints)
    market_api = MarketData.MarketAPI(
        api_key="",
        api_secret_key="",
        passphrase="",
        use_server_time=False,
        flag="0"
    )
    
    public_api = PublicData.PublicAPI(
        api_key="",
        api_secret_key="",
        passphrase="",
        use_server_time=False,
        flag="0"
    )
    
    print("🚀 Testing OKEx SDK Integration...")
    print("=" * 50)
    
    # Test 1: Get system time
    print("\n1. Testing system time...")
    try:
        result = public_api.get_system_time()
        if result and result.get('code') == '0':
            okex_time = result['data'][0]['ts']
            print(f"   ✅ OKEx Server Time: {okex_time}")
            print(f"   ✅ Local Time: {datetime.now().isoformat()}")
        else:
            print("   ❌ Failed to get system time")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get BTC-USDT ticker
    print("\n2. Testing ticker data...")
    try:
        result = market_api.get_ticker(instId="BTC-USDT")
        if result and result.get('code') == '0' and result.get('data'):
            data = result['data'][0]
            print(f"   ✅ BTC-USDT Price: ${data.get('last', 'N/A')}")
            print(f"   ✅ 24h Volume: {data.get('vol24h', 'N/A')}")
            print(f"   ✅ 24h High: ${data.get('high24h', 'N/A')}")
            print(f"   ✅ 24h Low: ${data.get('low24h', 'N/A')}")
        else:
            print("   ❌ Failed to get ticker data")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Get instruments
    print("\n3. Testing instruments...")
    try:
        result = public_api.get_instruments(instType="SPOT")
        if result and result.get('code') == '0':
            instruments_count = len(result['data'])
            print(f"   ✅ Found {instruments_count} SPOT instruments")
            # Show first 3 instruments as examples
            for i, instrument in enumerate(result['data'][:3]):
                print(f"   ✅ Example {i+1}: {instrument.get('instId', 'N/A')}")
        else:
            print("   ❌ Failed to get instruments")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 OKEx SDK Integration Test Complete!")
    print("\nYou can now use the following endpoints in your FastAPI app:")
    print("  • GET /okex/status - Check OKEx API status")
    print("  • GET /okex/ticker/BTC-USDT - Get ticker data")
    print("  • GET /okex/trading-pairs - Get popular trading pairs")
    print("  • GET /okex/instruments - Get trading instruments")
    print("  • GET /okex/orderbook/BTC-USDT - Get order book")
    print("  • GET /okex/kline/BTC-USDT?bar=1h&limit=24 - Get candlestick data")

if __name__ == "__main__":
    test_okex_integration()
