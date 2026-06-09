import React from 'react';

const DashboardCard = ({ title, value, icon: Icon, colorClass, trendText, trendType }) => {
  return (
    <div className="p-5 rounded-2xl glass-panel border border-white/5 flex items-center justify-between transition-all duration-300 hover:border-white/10 hover:bg-white/10 group">
      <div className="space-y-1 text-left">
        <span className="text-xs text-gray-400 font-semibold uppercase tracking-wider">{title}</span>
        <h3 className={`text-3xl font-extrabold ${colorClass}`}>{value}</h3>
        {trendText && (
          <div className="flex items-center gap-1.5 pt-1">
            <span className={`w-1.5 h-1.5 rounded-full ${trendType === 'danger' ? 'bg-rose-500 animate-pulse' : 'bg-emerald-500'}`} />
            <span className="text-[10px] text-gray-500 font-mono">{trendText}</span>
          </div>
        )}
      </div>
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center border transition-all duration-300 group-hover:scale-105 ${
        trendType === 'danger' 
          ? 'bg-rose-500/10 border-rose-500/20 text-rose-400 shadow-[0_0_15px_rgba(244,63,94,0.05)]' 
          : trendType === 'warning' 
            ? 'bg-amber-500/10 border-amber-500/20 text-amber-400'
            : 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400'
      }`}>
        <Icon className="w-6 h-6" />
      </div>
    </div>
  );
};

export default DashboardCard;
