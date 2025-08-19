import React from 'react';

const RecommendationsSection = ({ recommendations }) => {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getRecommendationColor = (grade) => {
    const lowerGrade = grade?.toLowerCase();
    if (lowerGrade?.includes('buy') || lowerGrade?.includes('outperform')) {
      return 'text-green-600 bg-green-100';
    } else if (lowerGrade?.includes('sell') || lowerGrade?.includes('underperform')) {
      return 'text-red-600 bg-red-100';
    } else if (lowerGrade?.includes('hold') || lowerGrade?.includes('neutral')) {
      return 'text-yellow-600 bg-yellow-100';
    }
    return 'text-gray-600 bg-gray-100';
  };

  if (!recommendations || recommendations.length === 0) {
    return (
      <div>
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Analyst Recommendations</h3>
        <p className="text-gray-600">No analyst recommendations available.</p>
      </div>
    );
  }

  const recentRecommendations = recommendations.slice(0, 10);

  const summary = recommendations.reduce((acc, rec) => {
    const grade = rec.To_Grade?.toLowerCase() || '';
    if (grade.includes('buy') || grade.includes('outperform')) {
      acc.buy++;
    } else if (grade.includes('sell') || grade.includes('underperform')) {
      acc.sell++;
    } else if (grade.includes('hold') || grade.includes('neutral')) {
      acc.hold++;
    }
    return acc;
  }, { buy: 0, hold: 0, sell: 0 });

  const total = summary.buy + summary.hold + summary.sell;

  return (
    <div>
      <h3 className="text-xl font-semibold text-gray-800 mb-4">Analyst Recommendations</h3>
      
      {total > 0 && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-3">Recommendation Summary</h4>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-green-600">{summary.buy}</div>
              <div className="text-sm text-gray-600">Buy</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-yellow-600">{summary.hold}</div>
              <div className="text-sm text-gray-600">Hold</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-red-600">{summary.sell}</div>
              <div className="text-sm text-gray-600">Sell</div>
            </div>
          </div>
          
          <div className="mt-4">
            <div className="flex rounded-full overflow-hidden h-3">
              {summary.buy > 0 && (
                <div 
                  className="bg-green-500" 
                  style={{width: `${(summary.buy / total) * 100}%`}}
                ></div>
              )}
              {summary.hold > 0 && (
                <div 
                  className="bg-yellow-500" 
                  style={{width: `${(summary.hold / total) * 100}%`}}
                ></div>
              )}
              {summary.sell > 0 && (
                <div 
                  className="bg-red-500" 
                  style={{width: `${(summary.sell / total) * 100}%`}}
                ></div>
              )}
            </div>
          </div>
        </div>
      )}

      <div className="space-y-3 max-h-80 overflow-y-auto">
        {recentRecommendations.map((rec, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-4">
            <div className="flex justify-between items-start mb-2">
              <div className="font-semibold text-gray-800">{rec.Firm}</div>
              <div className="text-sm text-gray-600">{formatDate(rec.Period)}</div>
            </div>
            
            <div className="flex items-center gap-3">
              {rec.From_Grade && (
                <span className="text-sm text-gray-600">
                  From: <span className="font-medium">{rec.From_Grade}</span>
                </span>
              )}
              <span className="text-gray-400">→</span>
              <span className={`px-2 py-1 rounded-full text-sm font-medium ${getRecommendationColor(rec.To_Grade)}`}>
                {rec.To_Grade}
              </span>
            </div>
            
            {rec.Action && (
              <div className="mt-2 text-sm text-gray-700">
                <span className="font-medium">Action:</span> {rec.Action}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationsSection;