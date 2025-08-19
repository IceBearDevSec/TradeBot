import requests
import logging
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class AlphaVantageService:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
        self.base_url = 'https://www.alphavantage.co/query'
        
    def get_stock_quote(self, symbol):
        """Get current stock quote"""
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'symbol': quote.get('01. symbol', symbol),
                    'current_price': float(quote.get('05. price', 0)),
                    'change': float(quote.get('09. change', 0)),
                    'change_percent': quote.get('10. change percent', '0%'),
                    'volume': int(quote.get('06. volume', 0)),
                    'latest_trading_day': quote.get('07. latest trading day'),
                    'previous_close': float(quote.get('08. previous close', 0)),
                    'open': float(quote.get('02. open', 0)),
                    'high': float(quote.get('03. high', 0)),
                    'low': float(quote.get('04. low', 0))
                }
            else:
                logger.error(f"No Global Quote data for {symbol}: {data}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {str(e)}")
            return None
    
    def get_daily_time_series(self, symbol, outputsize='compact'):
        """Get daily time series data"""
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': outputsize,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']
                dates = []
                prices = []
                
                # Sort dates and get last year of data
                sorted_dates = sorted(time_series.keys(), reverse=True)[:252]  # ~1 year
                
                for date in reversed(sorted_dates):
                    dates.append(date)
                    prices.append(float(time_series[date]['4. close']))
                
                return {
                    'dates': dates,
                    'prices': prices
                }
            else:
                logger.error(f"No time series data for {symbol}: {data}")
                return {'dates': [], 'prices': []}
                
        except Exception as e:
            logger.error(f"Error fetching time series for {symbol}: {str(e)}")
            return {'dates': [], 'prices': []}
    
    def get_company_overview(self, symbol):
        """Get company overview/fundamentals"""
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'Symbol' in data:
                return {
                    'company_name': data.get('Name', 'N/A'),
                    'sector': data.get('Sector', 'N/A'),
                    'industry': data.get('Industry', 'N/A'),
                    'market_cap': int(data.get('MarketCapitalization', 0)) if data.get('MarketCapitalization') != 'None' else None,
                    'pe_ratio': float(data.get('PERatio', 0)) if data.get('PERatio') != 'None' else None,
                    'dividend_yield': float(data.get('DividendYield', 0)) if data.get('DividendYield') != 'None' else None,
                    'fifty_two_week_high': float(data.get('52WeekHigh', 0)) if data.get('52WeekHigh') != 'None' else None,
                    'fifty_two_week_low': float(data.get('52WeekLow', 0)) if data.get('52WeekLow') != 'None' else None,
                    'summary': data.get('Description', 'No description available.')
                }
            else:
                logger.error(f"No overview data for {symbol}: {data}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching overview for {symbol}: {str(e)}")
            return None
    
    def search_symbol(self, keywords):
        """Search for symbols by keywords"""
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'bestMatches' in data:
                results = []
                for match in data['bestMatches'][:10]:  # Limit to 10 results
                    results.append({
                        'symbol': match.get('1. symbol'),
                        'name': match.get('2. name'),
                        'type': match.get('3. type'),
                        'region': match.get('4. region'),
                        'market_open': match.get('5. marketOpen'),
                        'market_close': match.get('6. marketClose'),
                        'timezone': match.get('7. timezone'),
                        'currency': match.get('8. currency'),
                        'match_score': match.get('9. matchScore')
                    })
                return results
            else:
                logger.error(f"No search results for {keywords}: {data}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching for {keywords}: {str(e)}")
            return []
    
    def get_news_sentiment(self, tickers=None, topics=None, limit=50):
        """Get news and sentiment data"""
        params = {
            'function': 'NEWS_SENTIMENT',
            'apikey': self.api_key,
            'limit': limit
        }
        
        if tickers:
            params['tickers'] = tickers
        if topics:
            params['topics'] = topics
            
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'feed' in data:
                news_items = []
                for item in data['feed'][:5]:  # Limit to 5 news items
                    news_items.append({
                        'title': item.get('title'),
                        'url': item.get('url'),
                        'time_published': item.get('time_published'),
                        'summary': item.get('summary'),
                        'source': item.get('source'),
                        'sentiment_score': item.get('overall_sentiment_score'),
                        'sentiment_label': item.get('overall_sentiment_label')
                    })
                return news_items
            else:
                logger.error(f"No news data: {data}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            return []