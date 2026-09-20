import React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle } from 'lucide-react';

const RiskBadge = ({ risk_level, size = 'sm' }) => {
  const level = risk_level?.toUpperCase() || 'LOW';
  
  const config = {
    LOW: {
      color: 'risk-low',
      icon: CheckCircle,
      text: 'LOW RISK'
    },
    MEDIUM: {
      color: 'risk-medium',
      icon: AlertTriangle,
      text: 'MEDIUM RISK'
    },
    HIGH: {
      color: 'risk-high',
      icon: AlertCircle,
      text: 'HIGH RISK',
      animate: size === 'lg' ? 'animate-pulse' : ''
    }
  };

  const { color, icon: Icon, text, animate } = config[level] || config.LOW;
  
  if (size === 'lg') {
    return (
      <div className={`flex flex-col items-center justify-center p-6 rounded-2xl ${color} ${animate || ''}`}>
        <Icon className="h-16 w-16 mb-4" />
        <span className="text-3xl font-bold tracking-wider">{text}</span>
      </div>
    );
  }

  return (
    <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold tracking-wide ${color}`}>
      <Icon className="h-3.5 w-3.5" />
      {text}
    </div>
  );
};

export default RiskBadge;
