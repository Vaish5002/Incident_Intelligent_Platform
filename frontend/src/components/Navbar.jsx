import React from 'react';
import { NavLink } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Terminal, ShieldCheck, Cpu, User, Menu } from 'lucide-react';

const Navbar = ({ onMenuClick }) => {
  const { activeIncidentId, setActiveIncidentId, incidents } = useApp();

  return (
    <nav className="sticky top-0 z-30 flex items-center justify-between px-6 h-16 border-b border-white/5 bg-bg-darker/60 backdrop-blur-md">
      
      {/* Brand logo and mobile controls */}
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="p-1.5 text-gray-400 rounded-lg md:hidden hover:bg-white/5 hover:text-gray-200 focus:outline-none"
        >
          <Menu className="w-6 h-6" />
        </button>

        <div className="flex items-center gap-2.5">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 text-indigo-400">
            <Terminal className="w-5 h-5 animate-pulse-slow" />
          </div>
          <span className="font-extrabold text-sm tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-violet-400">
            SMARTOPS AI
          </span>
        </div>
      </div>

      {/* Navigation center dropdown / context selectors */}
      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-2">
          <span className="text-[10px] text-gray-400 font-mono font-bold uppercase tracking-wider">Target:</span>
          <div className="relative">
            <select
              value={activeIncidentId}
              onChange={(e) => setActiveIncidentId(e.target.value)}
              className="pl-3 pr-8 py-1.5 text-xs font-mono font-bold rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-gray-200 outline-none cursor-pointer appearance-none min-w-[180px]"
            >
              {incidents.map((inc) => (
                <option key={inc.id} value={inc.id} className="bg-bg-darker text-gray-200">
                  {inc.id}: {inc.shortName}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Global status alert */}
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-semibold font-mono uppercase tracking-wider">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Active Control</span>
        </div>

        {/* Divider */}
        <div className="w-px h-5 bg-white/10"></div>

        {/* Profile indicator */}
        <div className="flex items-center gap-2">
          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 text-sm font-bold">
            S
          </div>
          <span className="hidden lg:inline text-xs font-bold text-gray-300">SRE Operator</span>
        </div>
      </div>

    </nav>
  );
};

export default Navbar;
