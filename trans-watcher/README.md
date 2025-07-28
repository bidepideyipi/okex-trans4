# FastAPI Demo with OKEx Integration

A FastAPI demonstration with basic CRUD operations and OKEx cryptocurrency exchange API integration.

## Features

- ✅ FastAPI framework with automatic API documentation
- ✅ Pydantic models for data validation
- ✅ Basic CRUD operations for items management
- ✅ **OKEx API Integration** for cryptocurrency data
- ✅ Interactive API documentation
- ✅ Health check endpoint
- ✅ Real-time cryptocurrency market data

## Project struture
/Users/anthony/fastapi_demo
├── main.py                   # Main application entry point
├── models                    # Model definitions
│   ├── __init__.py
│   ├── item_models.py        # Item models for CRUD
│   └── okex_models.py        # OKEx-related models
├── routers                   # API route handlers
│   ├── __init__.py
│   ├── candles.py            # Routes for candle data
│   ├── items.py              # Routes for items CRUD
│   └── okex.py               # Routes for OKEx data
├── services                  # Business logic and services
│   ├── __init__.py
│   ├── mongodb_service.py    # MongoDB service for data storage
│   └── okex_service.py       # OKEx service for data operations
├── test_candles_mongodb.py   # Test script for candles data and MongoDB
└── test_okex.py              # Test script for OKEx API integration

## Installation

1. **Create a virtual environment:**
```bash
python -m venv fastapi_env
```

2. **Activate the virtual environment:**
```bash
# On Windows
fastapi_env\Scripts\activate

# On macOS/Linux
source fastapi_env/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

```bash

source fastapi_env/bin/activate && python main.py
```

The API will be available at `http://localhost:8000`

## Testing OKEx Integration

Run the test script to verify OKEx API connectivity:
```bash
python test_okex.py
```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs:** `http://localhost:8000/docs`
- **Alternative API docs:** `http://localhost:8000/redoc`

## Available Endpoints

### Basic CRUD Operations
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /items` - Get all items
- `GET /items/{item_id}` - Get item by ID
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item
- `GET /items/search/{query}` - Search items by name

### OKEx Cryptocurrency API
- `GET /okex/status` - Check OKEx API connection status
- `GET /okex/ticker/{symbol}` - Get ticker data for a specific symbol (e.g., BTC-USDT)
- `GET /okex/trading-pairs` - Get popular trading pairs with current prices
- `GET /okex/instruments?instType=SPOT` - Get trading instruments
- `GET /okex/orderbook/{symbol}?sz=20` - Get order book for a symbol
- `GET /okex/kline/{symbol}?bar=1h&limit=24` - Get candlestick/kline data

## OKEx API Examples

### Get Bitcoin Price
```bash
curl "http://localhost:8000/okex/ticker/BTC-USDT"
```

### Get Popular Trading Pairs
```bash
curl "http://localhost:8000/okex/trading-pairs"
```

### Get Order Book
```bash
curl "http://localhost:8000/okex/orderbook/BTC-USDT?sz=10"
```

### Get Candlestick Data
```bash
curl "http://localhost:8000/okex/kline/ETH-USDT?bar=1h&limit=24"
```

## Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server for running the application
- **Pydantic** - Data validation using Python type hints
- **OKX** - Official OKEx API SDK for Python

## Notes

- The OKEx integration uses only **public endpoints** that don't require API credentials
- All cryptocurrency data is fetched in real-time from OKEx
- The application includes proper error handling for API failures
- All endpoints return JSON responses with consistent structure

