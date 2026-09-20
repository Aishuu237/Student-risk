import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, BookOpen, AlertTriangle, User } from 'lucide-react';
import axiosClient from '../api/axiosClient';
import { useAuth } from '../context/AuthContext';
import RiskBadge from '../components/RiskBadge';
import PerformanceChart from '../components/PerformanceChart';
import SubjectBar from '../components/SubjectBar';
import SuggestionCard from '../components/SuggestionCard';

const Dashboard = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await axiosClient.get('/students/me');
        setProfile(res.data);
        
        // If they have profile data, let's predict for suggestions
        if (res.data && res.data.attendance !== undefined) {
          try {
            const predRes = await axiosClient.post('/predict', {
              age: res.data.age || 18,
              study_time: res.data.study_time || 2,
              attendance: res.data.attendance || 80,
              previous_score: res.data.avg_score || 70,
              assignments: res.data.assignments || 5,
              internet_access: res.data.internet_access ?? true,
              extracurricular: res.data.extracurricular ?? false
            });
            setSuggestions(predRes.data.suggestions);
          } catch (e) {
            console.error("Failed to fetch suggestions", e);
          }
        }
      } catch (err) {
        console.error("Failed to fetch profile", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const dateStr = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });

  if (loading) {
    return (
      <div className="p-8 max-w-7xl mx-auto flex items-center justify-center min-h-[80vh]">
        <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="p-8 max-w-7xl mx-auto pt-24">
        <div className="card text-center py-16">
          <User className="h-16 w-16 text-slate-300 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-slate-800 mb-2">Welcome, {user?.name}!</h2>
          <p className="text-slate-500 mb-8 max-w-md mx-auto">
            We don't have your student profile data yet. Head over to the Prediction tool to analyze your current standing.
          </p>
          <button 
            onClick={() => navigate('/predict')}
            className="btn-primary inline-flex items-center gap-2"
          >
            <TrendingUp className="h-5 w-5" />
            Go to Predictor
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 mb-8">
        <div>
          <p className="text-slate-500 font-medium mb-1">{dateStr}</p>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
            Hello, {user?.name}! 👋
          </h1>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card flex items-center gap-4">
          <div className="p-4 bg-primary/10 rounded-xl text-primary">
            <BookOpen className="h-8 w-8" />
          </div>
          <div>
            <p className="text-slate-500 font-medium">Average Score</p>
            <p className="text-2xl font-bold text-slate-800">{profile.avg_score?.toFixed(1)}%</p>
          </div>
        </div>

        <div className="card flex items-center gap-4">
          <div className="p-4 bg-success/10 rounded-xl text-success">
            <TrendingUp className="h-8 w-8" />
          </div>
          <div>
            <p className="text-slate-500 font-medium">Attendance</p>
            <p className="text-2xl font-bold text-slate-800">{profile.attendance}%</p>
          </div>
        </div>

        <div className="card flex items-center justify-between">
          <div>
            <p className="text-slate-500 font-medium mb-2">Risk Level</p>
            <RiskBadge risk_level={profile.risk_level} />
          </div>
          <AlertTriangle className="h-10 w-10 text-slate-200" />
        </div>
      </div>

      <div className="w-full">
        <PerformanceChart scores={profile.subject_scores || []} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SubjectBar scores={profile.subject_scores || []} />
        <SuggestionCard suggestions={suggestions} risk_level={profile.risk_level} />
      </div>
    </div>
  );
};

export default Dashboard;
