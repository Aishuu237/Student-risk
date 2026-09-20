import React from 'react';
import { NavLink } from 'react-router-dom';
import { GraduationCap, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="fixed top-0 left-0 right-0 h-16 nav-gradient z-50 px-6 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <GraduationCap className="h-8 w-8 text-primary" />
        <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
          Student AI
        </span>
      </div>

      <div className="flex items-center gap-6 font-medium text-slate-600">
        <NavLink 
          to="/dashboard" 
          className={({ isActive }) => 
            `hover:text-primary transition-colors ${isActive ? 'text-primary' : ''}`
          }
        >
          Dashboard
        </NavLink>
        <NavLink 
          to="/predict" 
          className={({ isActive }) => 
            `hover:text-primary transition-colors ${isActive ? 'text-primary' : ''}`
          }
        >
          Predict
        </NavLink>
        {user?.role === 'admin' && (
          <NavLink 
            to="/admin" 
            className={({ isActive }) => 
              `hover:text-primary transition-colors ${isActive ? 'text-primary' : ''}`
            }
          >
            Admin Panel
          </NavLink>
        )}
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold">
            {user?.name?.charAt(0).toUpperCase()}
          </div>
          <span className="text-sm font-medium text-slate-700">{user?.name}</span>
        </div>
        <button 
          onClick={logout}
          className="p-2 text-slate-500 hover:text-danger hover:bg-danger/10 rounded-lg transition-colors"
          title="Logout"
        >
          <LogOut className="h-5 w-5" />
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
