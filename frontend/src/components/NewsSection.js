import React from 'react';

const NewsSection = ({ news }) => {
  const formatDate = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (!news || news.length === 0) {
    return (
      <div>
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Latest News</h3>
        <p className="text-gray-600">No recent news available.</p>
      </div>
    );
  }

  return (
    <div>
      <h3 className="text-xl font-semibold text-gray-800 mb-4">Latest News</h3>
      <div className="space-y-4 max-h-96 overflow-y-auto">
        {news.map((article, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <h4 className="font-semibold text-gray-800 mb-2 line-clamp-2">
              <a
                href={article.link}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-blue-600 transition-colors"
              >
                {article.title}
              </a>
            </h4>
            
            <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
              <span>{article.publisher}</span>
              <span>{formatDate(article.providerPublishTime)}</span>
            </div>
            
            {article.thumbnail && (
              <img
                src={article.thumbnail.resolutions?.[0]?.url}
                alt="Article thumbnail"
                className="w-full h-32 object-cover rounded mb-2"
              />
            )}
            
            <a
              href={article.link}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              Read more →
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NewsSection;