import React from 'react';
import { NavLink } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  LayoutDashboard, 
  UploadCloud, 
  Cpu, 
  FileText, 
  MessageSquare, 
  LogOut, 
  Terminal,
  Activity
} from 'lucide-react';

const Sidebar = ({ isOpen, toggleSidebar }) => {
  const { logout, activeIncident } = useApp();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Investigation Ingest', path: '/investigation', icon: UploadCloud },
    { name: 'Agent Results', path: '/results', icon: Cpu },
    { name: 'RCA Reports', path: '/reports', icon: FileText },
    { name: 'AI Copilot', path: '/copilot', icon: MessageSquare },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm md:hidden"
          onClick={toggleSidebar}
        />
      )}

      <aside className={`
        fixed top-0 bottom-0 left-0 z-50 flex flex-col w-64 border-r border-white/5 
        bg-bg-dark/85 backdrop-blur-xl transition-transform duration-300 md:translate-x-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        {/* Brand */}
        <div className="flex items-center gap-3 px-6 h-16 border-b border-white/5">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 text-indigo-400">
            <Terminal className="w-5 h-5 animate-pulse-slow" />
          </div>
          <div>
            <span className="font-extrabold text-base tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-violet-400">
              SMARTOPS AI
            </span>
            <div className="flex items-center gap-1.5 text-[9px] text-gray-400 font-mono">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping"></span>
              <span>AGENTIC ACTIVE</span>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              onClick={() => {
                if (window.innerWidth < 768) toggleSidebar();
              }}
              className={({ isActive }) => `
                flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group
                ${isActive 
                  ? 'bg-indigo-600/25 border border-indigo-500/30 text-indigo-200 shadow-glow-indigo' 
                  : 'text-gray-400 hover:bg-white/5 hover:text-gray-200 border border-transparent'}
              `}
            >
              <item.icon className="w-5 h-5 transition-transform group-hover:scale-110" />
              <span>{item.name}</span>
            </NavLink>
          ))}
        </nav>

        {/* Active Context Preview */}
        {activeIncident && (
          <div className="mx-4 my-2 p-3.5 rounded-xl bg-white/5 border border-white/5">
            <div className="text-[10px] text-gray-400 font-semibold tracking-wider uppercase mb-1">
              Active Context
            </div>
            <div className="text-xs font-semibold text-gray-200 truncate">
              {activeIncident.name}
            </div>
            <div className="flex items-center gap-2 mt-1.5">
              <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${
                activeIncident.severity === 'CRITICAL' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                activeIncident.severity === 'HIGH' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
              }`}>
                {activeIncident.severity}
              </span>
              <span className="text-[10px] text-gray-500 font-mono">
                {activeIncident.id}
              </span>
            </div>
          </div>
        )}

        {/* Footer / Logout */}
        <div className="p-4 border-t border-white/5">
          <button
            onClick={logout}
            className="flex items-center justify-between w-full px-4 py-3 text-sm font-medium text-gray-400 hover:text-rose-400 rounded-xl hover:bg-rose-500/5 transition-all duration-200 group border border-transparent"
          >
            <span className="flex items-center gap-3">
              <LogOut className="w-5 h-5 group-hover:translate-x-[-2px] transition-transform" />
              <span>Sign Out</span>
            </span>
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
