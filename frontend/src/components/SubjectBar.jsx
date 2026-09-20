import React from 'react';

const SubjectBar = ({ scores = [] }) => {
  const latestScores = Object.values(
    scores.reduce((acc, curr) => {
      if (!acc[curr.subject_name] || acc[curr.subject_name].term < curr.term) {
        acc[curr.subject_name] = curr;
      }
      return acc;
    }, {})
  ).sort((a, b) => b.score - a.score);

  const getScoreColor = (score) => {
    if (score >= 80) return 'bg-success';
    if (score >= 60) return 'bg-warning';
    return 'bg-danger';
  };

  return (
    <div className="card w-full">
      <h3 className="text-lg font-bold text-slate-800 mb-6">Latest Scores</h3>
      <div className="space-y-5">
        {latestScores.map((subject, idx) => (
          <div key={idx} className="w-full">
            <div className="flex justify-between items-end mb-2">
              <span className="font-medium text-slate-700">{subject.subject_name}</span>
              <span className="text-sm font-bold text-slate-900">{subject.score}%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div 
                className={`h-2.5 rounded-full ${getScoreColor(subject.score)} transition-all duration-1000 ease-out`}
                style={{ width: `${subject.score}%` }}
              ></div>
            </div>
          </div>
        ))}
        {latestScores.length === 0 && (
          <p className="text-slate-500 text-center py-4">No scores available</p>
        )}
      </div>
    </div>
  );
};

export default SubjectBar;
