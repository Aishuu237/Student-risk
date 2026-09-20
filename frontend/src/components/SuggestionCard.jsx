import React from 'react';
import { BrainCircuit } from 'lucide-react';

const icons = ['🎯', '📚', '⏰', '🏫', '💻', '🌟', '🧠', '✍️'];

const SuggestionCard = ({ suggestions = [], risk_level = 'LOW' }) => {
  const borderColors = {
    LOW: 'border-success',
    MEDIUM: 'border-warning',
    HIGH: 'border-danger'
  };
  
  const borderColor = borderColors[risk_level?.toUpperCase()] || borderColors.LOW;

  return (
    <div className={`card w-full border-t-4 animate-fade-in ${borderColor}`}>
      <div className="flex items-center gap-2 mb-6">
        <BrainCircuit className="h-6 w-6 text-primary" />
        <h3 className="text-lg font-bold text-slate-800">AI Recommendations</h3>
      </div>
      
      {suggestions.length > 0 ? (
        <ul className="space-y-4">
          {suggestions.map((suggestion, idx) => (
            <li key={idx} className="flex items-start gap-3">
              <span className="text-xl flex-shrink-0 mt-0.5">
                {icons[idx % icons.length]}
              </span>
              <p className="text-slate-600 leading-relaxed text-sm md:text-base">
                {suggestion}
              </p>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-slate-500 text-center py-4">No suggestions available at this time.</p>
      )}
    </div>
  );
};

export default SuggestionCard;
