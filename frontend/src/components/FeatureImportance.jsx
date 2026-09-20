import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

const FeatureImportance = ({ feature_importances = [] }) => {
  const data = feature_importances.map(f => ({
    name: f.feature.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
    importance: Math.round(f.importance * 100)
  })).sort((a, b) => b.importance - a.importance);

  return (
    <div className="card w-full h-[350px]">
      <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
        <span>🔍</span> Factors Affecting Risk
      </h3>
      <div className="w-full h-[250px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            layout="vertical"
            data={data}
            margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
            <XAxis type="number" domain={[0, 100]} hide />
            <YAxis 
              dataKey="name" 
              type="category" 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#475569', fontSize: 12 }}
            />
            <Tooltip
              formatter={(value) => [`${value}%`, 'Impact']}
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Bar 
              dataKey="importance" 
              fill="#8b5cf6" 
              radius={[0, 4, 4, 0]}
              barSize={20}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default FeatureImportance;
