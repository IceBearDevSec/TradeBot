# Trader Bot

A comprehensive stock analysis tool that provides real-time stock data, analyst recommendations, news, and interactive charts.

## Features

- **Real-time Stock Data**: Get current prices, market cap, P/E ratios, and more
- **Interactive Search**: Search for stocks, ETFs, and bonds with autocomplete
- **Price Charts**: 1-year price history with interactive charts
- **Analyst Recommendations**: View buy/hold/sell recommendations from financial firms
- **Latest News**: Recent news articles related to your selected stock
- **Detailed Metrics**: Comprehensive financial data including volume, price ranges, and company information

## Tech Stack

### Backend
- **Flask**: Python web framework
- **Alpha Vantage API**: Primary stock data provider (with Yahoo Finance fallback)
- **Flask-CORS**: Cross-origin resource sharing support
- **python-dotenv**: Environment variable management

### Frontend
- **React**: Frontend framework
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Interactive charts for price visualization
- **Axios**: HTTP client for API requests

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API Key (Optional but Recommended):
```bash
# Get your free API key from https://www.alphavantage.co/support/#api-key
# Edit backend/.env and replace 'demo' with your actual API key
ALPHA_VANTAGE_API_KEY=your_actual_api_key_here
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5001`

**Note**: The application works in demo mode with limited functionality. For full real-time data, get a free Alpha Vantage API key.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000` (or `http://localhost:3002` if 3000 is occupied)

## Usage

1. Start both the backend and frontend servers
2. Open your browser to `http://localhost:3000`
3. Use the search bar to find stocks, ETFs, or bonds
4. Click on search results or type a symbol directly
5. View comprehensive stock information including:
   - Current price and market data
   - Interactive price chart
   - Company summary
   - Analyst recommendations
   - Latest news articles

## API Endpoints

### Alpha Vantage Endpoints (Primary)
- `GET /api/av-stock/<symbol>`: Get comprehensive stock data using Alpha Vantage
- `GET /api/av-search/<query>`: Search for stocks using Alpha Vantage

### Fallback Endpoints
- `GET /api/stock/<symbol>`: Get stock data using Yahoo Finance (may hit rate limits)
- `GET /api/search/<query>`: Search using Yahoo Finance
- `GET /api/test/<symbol>`: Test endpoint with mock data
- `GET /api/health`: Health check endpoint

## Supported Assets

- **Stocks**: All major US and international stocks (e.g., AAPL, TSLA, GOOGL)
- **ETFs**: Exchange-traded funds (e.g., SPY, QQQ, VTI)
- **Bonds**: Bond ETFs and treasury securities (e.g., TLT, BND)

## Data Sources

### Primary: Alpha Vantage API
- **Real-time stock quotes**: Global market coverage with 20+ years of historical data
- **Company fundamentals**: Financial metrics, sector/industry information
- **News and sentiment**: Market news with sentiment analysis
- **Technical indicators**: 50+ technical analysis indicators
- **Free tier**: 25 API requests per day (upgrade available)

### Fallback: Yahoo Finance
- Used when Alpha Vantage is unavailable or rate-limited
- Comprehensive market data but subject to rate limiting

### Demo Mode
- Mock data for testing when APIs are unavailable
- Allows full UI testing without API dependencies

## Disclaimer

This tool is for educational and research purposes only. The data is sourced from Yahoo Finance and should not be used as the sole basis for investment decisions. Always consult with financial professionals before making investment choices.