import React, { useState, useEffect } from 'react';
import { Users, Search, ChevronRight, Activity, TrendingUp, X } from 'lucide-react';
import axiosClient from '../api/axiosClient';
import RiskBadge from '../components/RiskBadge';
import PerformanceChart from '../components/PerformanceChart';
import SubjectBar from '../components/SubjectBar';
import SuggestionCard from '../components/SuggestionCard';

const AdminPanel = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('ALL');
  
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [studentDetails, setStudentDetails] = useState(null);
  const [studentSuggestions, setStudentSuggestions] = useState([]);
  const [drawerLoading, setDrawerLoading] = useState(false);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const res = await axiosClient.get('/students/');
      setStudents(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRowClick = async (student) => {
    setSelectedStudent(student);
    setDrawerLoading(true);
    setStudentDetails(null);
    setStudentSuggestions([]);
    
    try {
      const res = await axiosClient.get(`/students/${student.id}`);
      setStudentDetails(res.data);
      
      const predRes = await axiosClient.post('/predict', {
        age: res.data.age || 18,
        study_time: res.data.study_time || 2,
        attendance: res.data.attendance || 80,
        previous_score: res.data.avg_score || 70,
        assignments: res.data.assignments || 5,
        internet_access: res.data.internet_access ?? true,
        extracurricular: res.data.extracurricular ?? false
      });
      setStudentSuggestions(predRes.data.suggestions);
    } catch (err) {
      console.error(err);
    } finally {
      setDrawerLoading(false);
    }
  };

  const filteredStudents = students.filter(s => {
    const name = s.name || s.user?.name || '';
    const email = s.email || s.user?.email || '';
    const matchesSearch = name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRisk = filterRisk === 'ALL' || s.risk_level === filterRisk;
    return matchesSearch && matchesRisk;
  });

  const stats = {
    total: students.length,
    highRisk: students.filter(s => s.risk_level === 'HIGH').length,
    avgScore: students.length ? students.reduce((acc, s) => acc + (s.avg_score || 0), 0) / students.length : 0
  };

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[80vh]">
        <div className="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 max-w-7xl mx-auto flex">
      <div className={`flex-1 transition-all duration-300 ${selectedStudent ? 'pr-4 md:mr-[500px]' : ''}`}>
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 flex items-center gap-3">
            <Users className="h-8 w-8 text-primary" />
            Admin Dashboard
          </h1>
          <p className="text-slate-500 mt-2">Manage and monitor student performance metrics.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card flex items-center gap-4">
            <div className="p-4 bg-primary/10 rounded-xl text-primary">
              <Users className="h-8 w-8" />
            </div>
            <div>
              <p className="text-slate-500 font-medium">Total Students</p>
              <p className="text-3xl font-bold text-slate-800">{stats.total}</p>
            </div>
          </div>
          <div className="card flex items-center gap-4 border-b-4 border-danger">
            <div className="p-4 bg-danger/10 rounded-xl text-danger">
              <Activity className="h-8 w-8" />
            </div>
            <div>
              <p className="text-slate-500 font-medium">High Risk Students</p>
              <p className="text-3xl font-bold text-slate-800">{stats.highRisk}</p>
            </div>
          </div>
          <div className="card flex items-center gap-4">
            <div className="p-4 bg-success/10 rounded-xl text-success">
              <TrendingUp className="h-8 w-8" />
            </div>
            <div>
              <p className="text-slate-500 font-medium">Global Avg Score</p>
              <p className="text-3xl font-bold text-slate-800">{stats.avgScore.toFixed(1)}%</p>
            </div>
          </div>
        </div>

        <div className="card p-0 overflow-hidden">
          <div className="p-4 border-b border-slate-200 flex flex-col sm:flex-row gap-4 justify-between bg-slate-50">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-slate-400" />
              <input
                type="text"
                placeholder="Search by name or email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
            <select
              value={filterRisk}
              onChange={(e) => setFilterRisk(e.target.value)}
              className="py-2 px-4 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-primary bg-white min-w-[150px]"
            >
              <option value="ALL">All Risk Levels</option>
              <option value="LOW">Low Risk</option>
              <option value="MEDIUM">Medium Risk</option>
              <option value="HIGH">High Risk</option>
            </select>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-100 text-slate-600 text-sm uppercase tracking-wider">
                  <th className="p-4 font-semibold">Student</th>
                  <th className="p-4 font-semibold">Avg Score</th>
                  <th className="p-4 font-semibold">Attendance</th>
                  <th className="p-4 font-semibold">Risk Level</th>
                  <th className="p-4 font-semibold"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {filteredStudents.length > 0 ? (
                  filteredStudents.map((student) => (
                    <tr 
                      key={student.id} 
                      onClick={() => handleRowClick(student)}
                      className={`hover:bg-slate-50 cursor-pointer transition-colors ${selectedStudent?.id === student.id ? 'bg-primary/5' : ''}`}
                    >
                      <td className="p-4">
                        <p className="font-bold text-slate-800">{student.name || student.user?.name}</p>
                        <p className="text-sm text-slate-500">{student.email || student.user?.email}</p>
                      </td>
                      <td className="p-4 font-medium">{student.avg_score?.toFixed(1)}%</td>
                      <td className="p-4">{student.attendance}%</td>
                      <td className="p-4">
                        <RiskBadge risk_level={student.risk_level} />
                      </td>
                      <td className="p-4 text-right text-slate-400">
                        <ChevronRight className="h-5 w-5 inline-block" />
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="p-8 text-center text-slate-500">
                      No students found matching your criteria.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Side Drawer */}
      {selectedStudent && (
        <div className="fixed inset-y-0 right-0 w-full md:w-[500px] bg-white shadow-2xl border-l border-slate-200 z-40 transform transition-transform duration-300 flex flex-col mt-16 pb-16">
          <div className="p-6 border-b border-slate-200 flex justify-between items-center bg-slate-50">
            <div>
              <h2 className="text-xl font-bold text-slate-800">{selectedStudent.name || selectedStudent.user?.name}</h2>
              <p className="text-sm text-slate-500">{selectedStudent.email || selectedStudent.user?.email}</p>
            </div>
            <button 
              onClick={() => setSelectedStudent(null)}
              className="p-2 hover:bg-slate-200 rounded-full transition-colors"
            >
              <X className="h-6 w-6 text-slate-500" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {drawerLoading ? (
              <div className="flex justify-center py-12">
                <div className="w-8 h-8 border-4 border-primary/30 border-t-primary rounded-full animate-spin"></div>
              </div>
            ) : studentDetails ? (
              <>
                <div className="flex justify-between items-center p-4 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="font-medium text-slate-600">Current Risk Level</span>
                  <RiskBadge risk_level={studentDetails.risk_level} />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 border border-slate-200 rounded-xl bg-white">
                    <p className="text-sm text-slate-500 mb-1">Study Time</p>
                    <p className="font-bold text-slate-800">{studentDetails.study_time} hrs/day</p>
                  </div>
                  <div className="p-4 border border-slate-200 rounded-xl bg-white">
                    <p className="text-sm text-slate-500 mb-1">Assignments</p>
                    <p className="font-bold text-slate-800">{studentDetails.assignments}/10</p>
                  </div>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
                  <PerformanceChart scores={studentDetails.subject_scores || []} />
                </div>
                
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
                  <SubjectBar scores={studentDetails.subject_scores || []} />
                </div>

                <SuggestionCard suggestions={studentSuggestions} risk_level={studentDetails.risk_level} />
              </>
            ) : (
              <p className="text-center text-slate-500 py-8">Failed to load student details.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;
