import os
import anthropic
import json
import logging
from typing import Dict, Any, Optional
from alpha_vantage_service import AlphaVantageService

logger = logging.getLogger(__name__)

class ClaudeService:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        self.av_service = AlphaVantageService()
    
    def process_natural_language_query(self, query: str) -> Dict[str, Any]:
        """Process a natural language query about stocks and trading"""
        try:
            # First, determine if the query is asking for specific stock data
            stock_context = self._get_stock_context_from_query(query)
            
            # Create the system prompt for financial analysis
            system_prompt = self._create_financial_analysis_prompt()
            
            # Format the user message with stock data if available
            user_message = self._format_user_message(query, stock_context)
            
            # Call Claude API
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            
            return {
                'response': response.content[0].text,
                'stock_data': stock_context,
                'query': query,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error processing natural language query: {str(e)}")
            return {
                'response': f"I'm sorry, I encountered an error processing your query: {str(e)}",
                'stock_data': None,
                'query': query,
                'success': False
            }
    
    def _get_stock_context_from_query(self, query: str) -> Optional[Dict[str, Any]]:
        """Extract stock symbols from query and fetch relevant data"""
        try:
            # Use Claude to extract stock symbols from the query
            symbol_extraction_prompt = """
            Extract any stock symbols (ticker symbols) mentioned in this query. 
            Return only the symbol(s) in uppercase, separated by commas if multiple.
            If no stock symbols are found, return "NONE".
            
            Query: {query}
            
            Stock symbols:""".format(query=query)
            
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=50,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": symbol_extraction_prompt
                    }
                ]
            )
            
            symbols_text = response.content[0].text.strip()
            
            if symbols_text == "NONE" or not symbols_text:
                return None
            
            # Get data for the first symbol found
            symbols = [s.strip() for s in symbols_text.split(',')]
            if symbols and symbols[0]:
                symbol = symbols[0]
                
                # Get stock data from Alpha Vantage
                quote_data = self.av_service.get_stock_quote(symbol)
                overview_data = self.av_service.get_company_overview(symbol)
                news_data = self.av_service.get_news_sentiment(tickers=symbol)
                
                return {
                    'symbol': symbol,
                    'quote': quote_data,
                    'overview': overview_data,
                    'news': news_data[:3] if news_data else []  # Limit to 3 recent news items
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting stock context: {str(e)}")
            return None
    
    def _create_financial_analysis_prompt(self) -> str:
        """Create the system prompt for financial analysis"""
        return """You are a knowledgeable financial advisor and stock market analyst. You provide helpful, accurate, and responsible financial information and analysis.

Key guidelines:
- Provide factual market analysis based on available data
- Never give specific buy/sell recommendations as financial advice
- Always remind users to do their own research and consult financial advisors
- Focus on educational content about market trends, company fundamentals, and general investment principles
- Use clear, accessible language while maintaining professional accuracy
- When discussing stocks, reference current data when available

If stock data is provided in the user's message, incorporate it into your analysis. Always emphasize that past performance doesn't guarantee future results."""
    
    def _format_user_message(self, query: str, stock_context: Optional[Dict[str, Any]]) -> str:
        """Format the user message with stock context if available"""
        if not stock_context:
            return f"User query: {query}"
        
        context_text = f"""User query: {query}

Current stock data for {stock_context['symbol']}:
"""
        
        if stock_context.get('quote'):
            quote = stock_context['quote']
            context_text += f"""
Price Information:
- Current Price: ${quote.get('current_price', 'N/A')}
- Change: {quote.get('change', 'N/A')} ({quote.get('change_percent', 'N/A')})
- Previous Close: ${quote.get('previous_close', 'N/A')}
- Volume: {quote.get('volume', 'N/A'):,} shares
"""
        
        if stock_context.get('overview'):
            overview = stock_context['overview']
            context_text += f"""
Company Information:
- Company: {overview.get('company_name', 'N/A')}
- Sector: {overview.get('sector', 'N/A')}
- Industry: {overview.get('industry', 'N/A')}
- Market Cap: ${overview.get('market_cap', 'N/A'):,} if overview.get('market_cap') else 'N/A'
- P/E Ratio: {overview.get('pe_ratio', 'N/A')}
"""
        
        if stock_context.get('news'):
            context_text += f"""
Recent News Headlines:
"""
            for news_item in stock_context['news']:
                context_text += f"- {news_item.get('title', 'N/A')}\n"
        
        return context_text