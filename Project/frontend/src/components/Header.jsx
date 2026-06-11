import React from 'react';
import { useApp } from '../context/AppContext';
import { Menu, ShieldCheck, ChevronDown, User, AlertCircle } from 'lucide-react';

const Header = ({ onMenuClick }) => {
  const { incidents, activeIncidentId, setActiveIncidentId, activeIncident, user } = useApp();

  return (
    <header className="sticky top-0 z-30 flex items-center justify-between px-6 h-16 border-b border-white/5 bg-bg-darker/60 backdrop-blur-md">
      
      {/* Mobile Toggle & breadcrumb */}
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="p-1.5 text-gray-400 rounded-lg md:hidden hover:bg-white/5 hover:text-gray-200 focus:outline-none"
        >
          <Menu className="w-6 h-6" />
        </button>
        
        {/* Incident Selector */}
        <div className="hidden sm:flex items-center gap-2">
          <span className="text-xs text-gray-400 font-mono font-medium uppercase tracking-wider">Context:</span>
          <div className="relative">
            <select
              value={activeIncidentId}
              onChange={(e) => setActiveIncidentId(e.target.value)}
              className="pl-3 pr-8 py-1.5 text-sm font-semibold rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-gray-200 outline-none cursor-pointer appearance-none min-w-[200px]"
            >
              {incidents.map((inc) => (
                <option key={inc.id} value={inc.id} className="bg-bg-darker text-gray-200">
                  {inc.id}: {inc.shortName}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-2.5 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Global Status & User Info */}
      <div className="flex items-center gap-4">
        {/* Mobile active incident indicator */}
        <div className="sm:hidden text-xs text-indigo-400 font-semibold px-2 py-1 rounded bg-indigo-500/10 border border-indigo-500/20">
          {activeIncidentId}
        </div>

        {/* Global status */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
          <ShieldCheck className="w-4 h-4" />
          <span>System Healthy</span>
        </div>

        {/* Active Incident Warning Badge */}
        {activeIncident && activeIncident.status !== 'RESOLVED' ? (
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-medium animate-pulse-slow">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>Active Incident</span>
          </div>
        ) : (
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-medium">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Mitigated</span>
          </div>
        )}

        {/* Vertical divider */}
        <div className="w-px h-5 bg-white/10"></div>

        {/* User Info */}
        <div className="flex items-center gap-2">
          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 text-sm font-semibold">
            {user?.name ? user.name[0] : 'O'}
          </div>
          <div className="hidden lg:block text-left">
            <div className="text-xs font-bold text-gray-200">{user?.name || 'SRE Operator'}</div>
            <div className="text-[10px] text-gray-400 font-mono">{user?.role || 'Incident Commander'}</div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
