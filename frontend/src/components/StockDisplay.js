import React from 'react';
import PriceChart from './PriceChart';
import NewsSection from './NewsSection';
import RecommendationsSection from './RecommendationsSection';

const StockDisplay = ({ stockData }) => {
  const formatCurrency = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  const formatNumber = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return new Intl.NumberFormat('en-US').format(value);
  };

  const formatPercentage = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return `${(value * 100).toFixed(2)}%`;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
      <div className="mb-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          {stockData.company_name} ({stockData.symbol})
        </h2>
        <div className="text-2xl font-semibold text-green-600 mb-4">
          {formatCurrency(stockData.current_price)}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Market Data</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Market Cap:</span>
              <span className="font-medium">{formatCurrency(stockData.market_cap)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Volume:</span>
              <span className="font-medium">{formatNumber(stockData.volume)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">P/E Ratio:</span>
              <span className="font-medium">{stockData.pe_ratio || 'N/A'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Dividend Yield:</span>
              <span className="font-medium">{formatPercentage(stockData.dividend_yield)}</span>
            </div>
          </div>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Price Range</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Day High:</span>
              <span className="font-medium">{formatCurrency(stockData.day_high)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Day Low:</span>
              <span className="font-medium">{formatCurrency(stockData.day_low)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">52W High:</span>
              <span className="font-medium">{formatCurrency(stockData.fifty_two_week_high)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">52W Low:</span>
              <span className="font-medium">{formatCurrency(stockData.fifty_two_week_low)}</span>
            </div>
          </div>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Company Info</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Sector:</span>
              <span className="font-medium">{stockData.sector || 'N/A'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Industry:</span>
              <span className="font-medium text-sm">{stockData.industry || 'N/A'}</span>
            </div>
          </div>
        </div>
      </div>

      {stockData.price_history && stockData.price_history.dates.length > 0 && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Price Chart (1 Year)</h3>
          <PriceChart priceHistory={stockData.price_history} />
        </div>
      )}

      {stockData.summary && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Company Summary</h3>
          <p className="text-gray-700 leading-relaxed">{stockData.summary}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <RecommendationsSection recommendations={stockData.recommendations} />
        <NewsSection news={stockData.news} />
      </div>
    </div>
  );
};

export default StockDisplay;