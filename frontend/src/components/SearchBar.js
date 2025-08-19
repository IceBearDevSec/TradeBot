import React, { useState, useEffect } from 'react';

const SearchBar = ({ onStockSelect }) => {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [searching, setSearching] = useState(false);

  useEffect(() => {
    const delayedSearch = setTimeout(() => {
      if (query.length > 1) {
        searchStocks(query);
      } else {
        setSearchResults([]);
        setShowResults(false);
      }
    }, 300);

    return () => clearTimeout(delayedSearch);
  }, [query]);

  const searchStocks = async (searchQuery) => {
    setSearching(true);
    try {
      // Try Alpha Vantage search first
      let response = await fetch(`/api/av-search/${searchQuery}`);
      
      if (!response.ok) {
        // Fall back to original search if available
        response = await fetch(`/api/search/${searchQuery}`);
      }
      
      if (response.ok) {
        const results = await response.json();
        setSearchResults(results);
        setShowResults(true);
      }
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setSearching(false);
    }
  };

  const handleSelect = (symbol) => {
    setQuery(symbol);
    setShowResults(false);
    onStockSelect(symbol);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      setShowResults(false);
      onStockSelect(query.trim().toUpperCase());
    }
  };

  return (
    <div className="relative mb-8">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <div className="flex-1 relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for stocks, ETFs, or bonds (e.g., AAPL, SPY, TLT)"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          
          {showResults && searchResults.length > 0 && (
            <div className="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-lg mt-1 shadow-lg z-10 max-h-64 overflow-y-auto">
              {searchResults.map((result, index) => (
                <div
                  key={index}
                  onClick={() => handleSelect(result.symbol)}
                  className="px-4 py-3 hover:bg-gray-100 cursor-pointer border-b border-gray-100 last:border-b-0"
                >
                  <div className="font-semibold text-blue-600">{result.symbol}</div>
                  <div className="text-sm text-gray-600">
                    {result.name} • {result.type} • {result.exchange}
                  </div>
                </div>
              ))}
            </div>
          )}
          
          {searching && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            </div>
          )}
        </div>
        
        <button
          type="submit"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Search
        </button>
      </form>
    </div>
  );
};

export default SearchBar;