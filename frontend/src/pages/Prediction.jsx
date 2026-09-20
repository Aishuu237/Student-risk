import React, { useState, useEffect } from 'react';
import { Sparkles } from 'lucide-react';
import axiosClient from '../api/axiosClient';
import RiskBadge from '../components/RiskBadge';
import FeatureImportance from '../components/FeatureImportance';
import SuggestionCard from '../components/SuggestionCard';

const Prediction = () => {
  const [formData, setFormData] = useState({
    age: 18,
    study_time: 2,
    attendance: 80,
    previous_score: 70,
    assignments: 5,
    internet_access: true,
    extracurricular: false
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    // Try to pre-fill with student data
    axiosClient.get('/students/me').then((res) => {
      if (res.data) {
        setFormData(prev => ({
          ...prev,
          age: res.data.age || prev.age,
          study_time: res.data.study_time || prev.study_time,
          attendance: res.data.attendance || prev.attendance,
          previous_score: res.data.avg_score || prev.previous_score,
          assignments: res.data.assignments || prev.assignments,
          internet_access: res.data.internet_access ?? prev.internet_access,
          extracurricular: res.data.extracurricular ?? prev.extracurricular
        }));
      }
    }).catch(() => {
      // Ignore if no profile or not a student
    });
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : Number(value)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const res = await axiosClient.post('/predict', formData);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to predict. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 md:p-8 max-w-5xl mx-auto space-y-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-slate-800 mb-3 flex items-center justify-center gap-3">
          <span className="text-4xl">🤖</span> AI Risk Prediction
        </h1>
        <p className="text-slate-500 max-w-xl mx-auto">
          Enter your current academic metrics to get an AI-powered prediction of your performance risk and personalized recommendations.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-5">
          <div className="card sticky top-24">
            <h2 className="text-xl font-bold text-slate-800 mb-6 border-b pb-4">Metrics Input</h2>
            
            {error && (
              <div className="mb-6 p-4 rounded-lg bg-danger/10 border border-danger/20 text-danger text-sm">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Age</label>
                  <input
                    type="number" name="age" min="15" max="30"
                    value={formData.age} onChange={handleChange}
                    className="w-full border border-slate-200 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Prev Score</label>
                  <input
                    type="number" name="previous_score" min="0" max="100"
                    value={formData.previous_score} onChange={handleChange}
                    className="w-full border border-slate-200 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <label className="text-sm font-medium text-slate-700">Study Time (hrs/day)</label>
                  <span className="text-sm font-bold text-primary">{formData.study_time} hrs</span>
                </div>
                <input
                  type="range" name="study_time" min="0" max="10" step="0.5"
                  value={formData.study_time} onChange={handleChange}
                  className="w-full accent-primary"
                />
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <label className="text-sm font-medium text-slate-700">Attendance %</label>
                  <span className={`text-sm font-bold ${formData.attendance >= 80 ? 'text-success' : formData.attendance >= 60 ? 'text-warning' : 'text-danger'}`}>
                    {formData.attendance}%
                  </span>
                </div>
                <input
                  type="range" name="attendance" min="0" max="100"
                  value={formData.attendance} onChange={handleChange}
                  className="w-full accent-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Assignments Done (out of 10)</label>
                <input
                  type="number" name="assignments" min="0" max="10"
                  value={formData.assignments} onChange={handleChange}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                />
              </div>

              <div className="grid grid-cols-2 gap-4 pt-2">
                <label className="flex items-center gap-3 p-3 border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-50 transition-colors">
                  <input
                    type="checkbox" name="internet_access"
                    checked={formData.internet_access} onChange={handleChange}
                    className="w-4 h-4 text-primary rounded focus:ring-primary accent-primary"
                  />
                  <span className="text-sm font-medium text-slate-700">Internet Access</span>
                </label>
                <label className="flex items-center gap-3 p-3 border border-slate-200 rounded-lg cursor-pointer hover:bg-slate-50 transition-colors">
                  <input
                    type="checkbox" name="extracurricular"
                    checked={formData.extracurricular} onChange={handleChange}
                    className="w-4 h-4 text-primary rounded focus:ring-primary accent-primary"
                  />
                  <span className="text-sm font-medium text-slate-700">Extracurricular</span>
                </label>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary py-3 text-lg flex items-center justify-center gap-2"
              >
                {loading ? (
                  <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                ) : (
                  <>
                    <Sparkles className="h-5 w-5" />
                    Predict Risk
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        <div className="lg:col-span-7 space-y-6">
          {!result && !loading && (
            <div className="h-full min-h-[400px] flex flex-col items-center justify-center border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/50 p-8 text-center">
              <div className="text-6xl mb-4 opacity-50">🔮</div>
              <h3 className="text-xl font-bold text-slate-700 mb-2">Awaiting Input</h3>
              <p className="text-slate-500 max-w-sm">
                Fill out the metrics on the left and click predict to see your personalized AI analysis.
              </p>
            </div>
          )}

          {result && (
            <div className="space-y-6 animate-fade-in">
              <div className="card flex flex-col items-center justify-center py-8">
                <p className="text-slate-500 font-medium mb-4 uppercase tracking-wider">Predicted Outcome</p>
                <RiskBadge risk_level={result.risk_level} size="lg" />
                <div className="mt-6 w-full max-w-md">
                  <div className="flex justify-between text-sm font-medium text-slate-600 mb-2">
                    <span>AI Confidence</span>
                    <span>{Math.round(result.confidence)}%</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                    <div 
                      className="bg-primary h-2 rounded-full transition-all duration-1000" 
                      style={{ width: `${result.confidence}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="md:col-span-2">
                  <SuggestionCard suggestions={result.suggestions} risk_level={result.risk_level} />
                </div>
                <div className="md:col-span-2">
                  <FeatureImportance feature_importances={result.feature_importances} />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Prediction;
