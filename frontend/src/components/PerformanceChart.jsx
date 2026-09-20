import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const colors = ['#6366f1', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];

const PerformanceChart = ({ scores = [] }) => {
  // Process data to group by term
  const dataMap = scores.reduce((acc, curr) => {
    if (!acc[curr.term]) {
      acc[curr.term] = { term: curr.term };
    }
    acc[curr.term][curr.subject_name] = curr.score;
    return acc;
  }, {});

  const data = Object.values(dataMap).sort((a, b) => a.term.localeCompare(b.term));
  
  // Extract all unique subjects
  const subjects = [...new Set(scores.map(s => s.subject_name))];

  return (
    <div className="card w-full h-[400px]">
      <h3 className="text-lg font-bold text-slate-800 mb-6">Performance Trend</h3>
      <div className="w-full h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis 
              dataKey="term" 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b' }}
              dy={10}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#64748b' }}
              domain={[0, 100]}
              dx={-10}
            />
            <Tooltip
              contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
            />
            <Legend wrapperStyle={{ paddingTop: '20px' }} />
            {subjects.map((subject, index) => (
              <Line
                key={subject}
                type="monotone"
                dataKey={subject}
                stroke={colors[index % colors.length]}
                strokeWidth={3}
                dot={{ r: 4, strokeWidth: 2 }}
                activeDot={{ r: 6 }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PerformanceChart;
