import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import StockDisplay from './components/StockDisplay';
import './App.css';

function App() {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleStockSelect = async (symbol) => {
    setLoading(true);
    setError(null);
    
    try {
      // Try Alpha Vantage first, fall back to test data if needed
      let response = await fetch(`/api/av-stock/${symbol}`);
      
      if (!response.ok) {
        // Fall back to test endpoint
        response = await fetch(`/api/test/${symbol}`);
        if (!response.ok) {
          throw new Error('Failed to fetch stock data');
        }
      }
      
      const data = await response.json();
      setStockData(data);
    } catch (err) {
      setError(err.message);
      setStockData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-4">
          Trader Bot
        </h1>
        
        <div className="max-w-4xl mx-auto mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-800 text-sm">
            <strong>✅ Live Data Active:</strong> Connected to Alpha Vantage API with real-time stock data, news, and market information.
          </p>
        </div>
        
        <div className="max-w-4xl mx-auto">
          <SearchBar onStockSelect={handleStockSelect} />
          
          {loading && (
            <div className="text-center py-8">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p className="mt-2 text-gray-600">Loading stock data...</p>
            </div>
          )}
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mt-4">
              Error: {error}
            </div>
          )}
          
          {stockData && !loading && (
            <StockDisplay stockData={stockData} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;