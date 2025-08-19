from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import logging
import time
import os
from functools import wraps
from dotenv import load_dotenv
from alpha_vantage_service import AlphaVantageService
from claude_service import ClaudeService

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
av_service = AlphaVantageService()
claude_service = ClaudeService()

def retry_on_rate_limit(retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "429" in str(e) and attempt < retries - 1:
                        logger.warning(f"Rate limited, retrying in {delay} seconds...")
                        time.sleep(delay)
                        delay *= 2
                    else:
                        raise e
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/stock/<symbol>', methods=['GET'])
@retry_on_rate_limit()
def get_stock_data(symbol):
    try:
        # Add a longer delay to avoid rate limiting
        time.sleep(2)
        
        # Create ticker with custom session
        import requests
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        ticker = yf.Ticker(symbol, session=session)
        
        info = ticker.info
        history = ticker.history(period="1y")
        
        try:
            news = ticker.news
        except:
            news = []
            
        try:
            recommendations = ticker.recommendations
        except:
            recommendations = None
        
        current_price = history['Close'].iloc[-1] if not history.empty else None
        
        response_data = {
            'symbol': symbol.upper(),
            'current_price': float(current_price) if current_price else None,
            'company_name': info.get('longName', symbol.upper()),
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'dividend_yield': info.get('dividendYield'),
            'volume': info.get('volume'),
            'day_high': info.get('dayHigh'),
            'day_low': info.get('dayLow'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'summary': info.get('longBusinessSummary'),
            'news': news[:5] if news else [],
            'recommendations': recommendations.to_dict('records') if recommendations is not None and not recommendations.empty else [],
            'price_history': {
                'dates': [str(date.date()) for date in history.index],
                'prices': history['Close'].tolist()
            } if not history.empty else {'dates': [], 'prices': []}
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return jsonify({'error': f'Failed to fetch data for {symbol}'}), 400

@app.route('/api/search/<query>', methods=['GET'])
def search_stocks(query):
    try:
        import yfinance as yf
        
        search_results = yf.Search(query)
        quotes = search_results.quotes[:10]
        
        results = []
        for quote in quotes:
            results.append({
                'symbol': quote.get('symbol'),
                'name': quote.get('longname') or quote.get('shortname'),
                'type': quote.get('quoteType'),
                'exchange': quote.get('exchange')
            })
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error searching for {query}: {str(e)}")
        return jsonify({'error': f'Failed to search for {query}'}), 400

@app.route('/api/av-stock/<symbol>', methods=['GET'])
def get_alpha_vantage_stock_data(symbol):
    """Get stock data using Alpha Vantage API"""
    try:
        logger.info(f"Fetching data for {symbol} using Alpha Vantage")
        
        # Get stock quote
        quote_data = av_service.get_stock_quote(symbol)
        if not quote_data:
            return jsonify({'error': f'No quote data found for {symbol}'}), 404
        
        # Get company overview
        overview_data = av_service.get_company_overview(symbol)
        
        # Get historical data
        historical_data = av_service.get_daily_time_series(symbol)
        
        # Get news
        news_data = av_service.get_news_sentiment(tickers=symbol)
        
        # Combine all data
        response_data = {
            'symbol': quote_data['symbol'],
            'current_price': quote_data['current_price'],
            'company_name': overview_data['company_name'] if overview_data else f'{symbol} Company',
            'market_cap': overview_data['market_cap'] if overview_data else None,
            'pe_ratio': overview_data['pe_ratio'] if overview_data else None,
            'dividend_yield': overview_data['dividend_yield'] if overview_data else None,
            'volume': quote_data['volume'],
            'day_high': quote_data['high'],
            'day_low': quote_data['low'],
            'fifty_two_week_high': overview_data['fifty_two_week_high'] if overview_data else None,
            'fifty_two_week_low': overview_data['fifty_two_week_low'] if overview_data else None,
            'sector': overview_data['sector'] if overview_data else 'N/A',
            'industry': overview_data['industry'] if overview_data else 'N/A',
            'summary': overview_data['summary'] if overview_data else 'No description available.',
            'news': [
                {
                    'title': item['title'],
                    'link': item['url'],
                    'publisher': item['source'],
                    'providerPublishTime': item['time_published'],
                    'summary': item['summary']
                } for item in news_data
            ],
            'recommendations': [
                {
                    'Firm': 'Alpha Vantage Sentiment Analysis',
                    'To_Grade': news_data[0]['sentiment_label'] if news_data else 'Neutral',
                    'Action': 'sentiment',
                    'Period': quote_data['latest_trading_day']
                }
            ] if news_data else [],
            'price_history': historical_data,
            'change': quote_data['change'],
            'change_percent': quote_data['change_percent'],
            'previous_close': quote_data['previous_close'],
            'open': quote_data['open']
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error fetching Alpha Vantage data for {symbol}: {str(e)}")
        return jsonify({'error': f'Failed to fetch data for {symbol}'}), 500

@app.route('/api/av-search/<query>', methods=['GET'])
def search_alpha_vantage_stocks(query):
    """Search for stocks using Alpha Vantage"""
    try:
        results = av_service.search_symbol(query)
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                'symbol': result['symbol'],
                'name': result['name'],
                'type': result['type'],
                'exchange': f"{result['region']} - {result['currency']}"
            })
        
        return jsonify(formatted_results)
        
    except Exception as e:
        logger.error(f"Error searching for {query}: {str(e)}")
        return jsonify({'error': f'Failed to search for {query}'}), 500

@app.route('/api/test/<symbol>', methods=['GET'])
def get_test_stock_data(symbol):
    """Test endpoint with mock data"""
    mock_data = {
        'symbol': symbol.upper(),
        'current_price': 150.25,
        'company_name': f'{symbol.upper()} Test Company Inc.',
        'market_cap': 2500000000000,
        'pe_ratio': 25.4,
        'dividend_yield': 0.024,
        'volume': 45678901,
        'day_high': 152.30,
        'day_low': 148.90,
        'fifty_two_week_high': 180.95,
        'fifty_two_week_low': 125.20,
        'sector': 'Technology',
        'industry': 'Consumer Electronics',
        'summary': 'This is a test company for demonstration purposes.',
        'news': [
            {
                'title': f'{symbol.upper()} reaches new highs amid strong earnings',
                'publisher': 'Test News Network',
                'link': 'https://example.com/test',
                'providerPublishTime': 1692460800,
                'thumbnail': {
                    'resolutions': [{'url': 'https://via.placeholder.com/150x100'}]
                }
            }
        ],
        'recommendations': [
            {
                'Firm': 'Test Investment Bank',
                'To_Grade': 'Buy',
                'From_Grade': 'Hold',
                'Action': 'up',
                'Period': '2024-01-15'
            }
        ],
        'price_history': {
            'dates': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01'],
            'prices': [140.5, 145.2, 148.8, 150.25]
        }
    }
    return jsonify(mock_data)

@app.route('/api/nlp-query', methods=['POST'])
def process_natural_language_query():
    """Process natural language queries about stocks and trading"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        logger.info(f"Processing NLP query: {query}")
        
        # Process the query using Claude
        result = claude_service.process_natural_language_query(query)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing NLP query: {str(e)}")
        return jsonify({'error': f'Failed to process query: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)