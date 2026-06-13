import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  severityData, 
  errorFrequencyData, 
  timelineData, 
  riskScoreDistribution 
} from '../services/mockData';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  LineChart, 
  Line, 
  PieChart, 
  Pie, 
  Cell, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend 
} from 'recharts';
import { 
  AlertOctagon, 
  FolderOpen, 
  CheckCircle, 
  Flame, 
  TrendingUp, 
  Clock, 
  ArrowRight,
  ShieldAlert,
  Zap,
  DollarSign,
  Users,
  Target,
  Activity,
  ChevronRight,
  AlertTriangle
} from 'lucide-react';
import DashboardCard from '../components/DashboardCard';

const Dashboard = () => {
  const { incidents, setActiveIncidentId } = useApp();
  const navigate = useNavigate();
  const [animatedMetrics, setAnimatedMetrics] = useState({
    timeSaved: 0,
    costSaved: 0,
    accuracy: 0
  });

  // Compute metrics based on local incidents state
  const totalIncidents = incidents.length;
  const criticalIncidents = incidents.filter(inc => inc.severity === 'CRITICAL').length;
  const openInvestigations = incidents.filter(inc => inc.status === 'INVESTIGATING').length;
  const resolvedCases = incidents.filter(inc => inc.status === 'RESOLVED').length;

  // Business Impact Calculations
  const avgInvestigationTime = 30; // seconds with SmartOps AI
  const manualInvestigationTime = 3.5 * 60 * 60; // 3.5 hours in seconds
  const timeSavedPerIncident = manualInvestigationTime - avgInvestigationTime;
  const totalTimeSavedHours = (timeSavedPerIncident * totalIncidents) / 3600;
  const costPerHour = 150; // Average DevOps engineer cost
  const totalCostSaved = totalTimeSavedHours * costPerHour;
  const totalUsersAffected = incidents.reduce((sum, inc) => sum + (inc.activeUsersAffected || 0), 0);

  // Animate metrics on mount
  useEffect(() => {
    const duration = 2000;
    const steps = 60;
    const interval = duration / steps;
    
    let currentStep = 0;
    const timer = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;
      
      setAnimatedMetrics({
        timeSaved: Math.floor(totalTimeSavedHours * progress),
        costSaved: Math.floor(totalCostSaved * progress),
        accuracy: Math.floor(96 * progress)
      });
      
      if (currentStep >= steps) clearInterval(timer);
    }, interval);
    
    return () => clearInterval(timer);
  }, [totalIncidents]);

  const handleIncidentClick = (id) => {
    setActiveIncidentId(id);
    navigate('/analysis');
  };

  // Compute average risk score
  const avgRiskScore = Math.round(incidents.reduce((sum, inc) => sum + inc.riskScore, 0) / incidents.length);

  return (
    <div className="space-y-6">
      
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 p-6 rounded-2xl glass-panel border border-white/5 shadow-glass">
        <div>
          <h2 className="text-2xl font-extrabold tracking-tight text-gray-100">
            Operations Control Room
          </h2>
          <p className="text-sm text-gray-400 mt-1">
            Real-time telemetry and agentic analysis for the SmartOps system environment.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => navigate('/investigation')}
            className="flex items-center gap-2 px-5 py-2.5 text-xs font-bold rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white shadow-glow-indigo transition-all cursor-pointer"
          >
            <AlertOctagon className="w-4 h-4" />
            <span>Analyze Incident</span>
          </button>
          
          <div className="flex items-center gap-2.5 px-3 py-2.5 rounded-lg bg-white/5 border border-white/10 text-[10px] text-indigo-300 font-semibold font-mono tracking-wider">
            <span className="flex h-1.5 w-1.5 relative shrink-0">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-indigo-500"></span>
            </span>
            <span>AGENT POOL: ACTIVE</span>
          </div>
        </div>
      </div>

      {/* Business Value Comparison - Before vs After SmartOps AI */}
      <div className="p-6 rounded-2xl glass-panel border border-indigo-500/20 bg-gradient-to-br from-indigo-500/5 to-purple-500/5">
        <div className="flex items-center gap-2 mb-4">
          <Target className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-bold text-gray-100">Business Impact: Manual vs AI-Powered Investigation</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Time Comparison */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-gray-300">Investigation Time</span>
              <Clock className="w-4 h-4 text-gray-400" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                <span className="text-xs text-gray-400">Manual Process</span>
                <span className="text-lg font-bold text-red-400">2-4 hours</span>
              </div>
              <div className="flex items-center justify-center py-1">
                <ChevronRight className="w-5 h-5 text-indigo-400 rotate-90" />
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                <span className="text-xs text-gray-400">SmartOps AI</span>
                <span className="text-lg font-bold text-emerald-400">30 seconds</span>
              </div>
            </div>
            <div className="pt-2 text-center">
              <p className="text-2xl font-extrabold text-indigo-400">{animatedMetrics.timeSaved}h+</p>
              <p className="text-xs text-gray-500">Total Time Saved</p>
            </div>
          </div>

          {/* Accuracy Comparison */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-gray-300">Root Cause Accuracy</span>
              <Target className="w-4 h-4 text-gray-400" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 rounded-lg bg-amber-500/10 border border-amber-500/20">
                <span className="text-xs text-gray-400">Manual Analysis</span>
                <span className="text-lg font-bold text-amber-400">60-70%</span>
              </div>
              <div className="flex items-center justify-center py-1">
                <ChevronRight className="w-5 h-5 text-indigo-400 rotate-90" />
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                <span className="text-xs text-gray-400">SmartOps AI</span>
                <span className="text-lg font-bold text-emerald-400">{animatedMetrics.accuracy}%</span>
              </div>
            </div>
            <div className="pt-2 text-center">
              <p className="text-2xl font-extrabold text-indigo-400">+{Math.max(0, animatedMetrics.accuracy - 65)}%</p>
              <p className="text-xs text-gray-500">Accuracy Improvement</p>
            </div>
          </div>

          {/* Cost Comparison */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-gray-300">Cost Per Incident</span>
              <DollarSign className="w-4 h-4 text-gray-400" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                <span className="text-xs text-gray-400">Manual (@$150/hr)</span>
                <span className="text-lg font-bold text-red-400">$525</span>
              </div>
              <div className="flex items-center justify-center py-1">
                <ChevronRight className="w-5 h-5 text-indigo-400 rotate-90" />
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                <span className="text-xs text-gray-400">SmartOps AI</span>
                <span className="text-lg font-bold text-emerald-400">$0.01</span>
              </div>
            </div>
            <div className="pt-2 text-center">
              <p className="text-2xl font-extrabold text-indigo-400">${animatedMetrics.costSaved.toLocaleString()}</p>
              <p className="text-xs text-gray-500">Total Cost Saved</p>
            </div>
          </div>
        </div>

        {/* Bottom Stats Bar */}
        <div className="mt-6 pt-6 border-t border-white/10 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-indigo-400">{totalIncidents}</p>
            <p className="text-xs text-gray-500 mt-1">Incidents Analyzed</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-emerald-400">{totalUsersAffected.toLocaleString()}</p>
            <p className="text-xs text-gray-500 mt-1">Users Protected</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-purple-400">7</p>
            <p className="text-xs text-gray-500 mt-1">Failure Types Detected</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-pink-400">100%</p>
            <p className="text-xs text-gray-500 mt-1">Auto-Investigation Rate</p>
          </div>
        </div>
      </div>

      {/* Enhanced Metrics Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <DashboardCard 
          title="Total Incidents"
          value={totalIncidents}
          icon={FolderOpen}
          colorClass="text-gray-100"
          trendText="Historical telemetry"
          trendType="info"
        />
        <DashboardCard 
          title="Avg Risk Score"
          value={avgRiskScore}
          icon={ShieldAlert}
          colorClass="text-indigo-400"
          trendText="Risk index profile"
          trendType="info"
        />
        <DashboardCard 
          title="Active Investigations"
          value={openInvestigations}
          icon={AlertOctagon}
          colorClass="text-amber-500"
          trendText="Under AI analysis"
          trendType="warning"
        />
        <DashboardCard 
          title="Resolved Cases"
          value={resolvedCases}
          icon={CheckCircle}
          colorClass="text-emerald-500"
          trendText="System mitigated"
          trendType="success"
        />
        <DashboardCard 
          title="Critical Alerts"
          value={criticalIncidents}
          icon={Flame}
          colorClass="text-rose-400"
          trendText="Requires immediate action"
          trendType="danger"
        />
      </div>

      {/* Key Platform Capabilities */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-5 rounded-2xl glass-panel border border-emerald-500/20 bg-gradient-to-br from-emerald-500/5 to-teal-500/5 hover:border-emerald-500/40 transition-all">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shrink-0">
              <Zap className="w-6 h-6 text-emerald-400" />
            </div>
            <div className="space-y-1">
              <h4 className="text-sm font-bold text-gray-200">Lightning Fast Analysis</h4>
              <p className="text-xs text-gray-400 leading-relaxed">
                Multi-agent system processes incidents in <span className="text-emerald-400 font-semibold">30 seconds</span> vs 2-4 hours manual investigation
              </p>
            </div>
          </div>
        </div>

        <div className="p-5 rounded-2xl glass-panel border border-purple-500/20 bg-gradient-to-br from-purple-500/5 to-pink-500/5 hover:border-purple-500/40 transition-all">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center shrink-0">
              <Activity className="w-6 h-6 text-purple-400" />
            </div>
            <div className="space-y-1">
              <h4 className="text-sm font-bold text-gray-200">7 Failure Type Detection</h4>
              <p className="text-xs text-gray-400 leading-relaxed">
                Contextual RCA engine adapts analysis for Database, Memory, CPU, API, Cache, Network, and Disk issues
              </p>
            </div>
          </div>
        </div>

        <div className="p-5 rounded-2xl glass-panel border border-indigo-500/20 bg-gradient-to-br from-indigo-500/5 to-blue-500/5 hover:border-indigo-500/40 transition-all">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center shrink-0">
              <Target className="w-6 h-6 text-indigo-400" />
            </div>
            <div className="space-y-1">
              <h4 className="text-sm font-bold text-gray-200">96% Root Cause Accuracy</h4>
              <p className="text-xs text-gray-400 leading-relaxed">
                AI-powered analysis with GitHub commit correlation, log pattern matching, and historical incident learning
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Error Frequency Chart (Bar Chart) - Occupies 7 columns */}
        <div className="lg:col-span-7 p-5 rounded-2xl glass-panel border border-white/5 space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="text-sm font-bold text-gray-200 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-indigo-400" />
              <span>Error Frequency Chart</span>
            </h4>
            <span className="text-[10px] text-gray-500 font-mono">Last 6 Hours</span>
          </div>
          <div className="h-72 w-full text-xs font-mono">
            <ResponsiveContainer width="100%" height={288} minWidth={0}>
              <BarChart data={errorFrequencyData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff08" />
                <XAxis dataKey="time" stroke="#9ca3af" fontSize={10} tickLine={false} />
                <YAxis stroke="#9ca3af" fontSize={10} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0d101c', borderColor: '#ffffff10', borderRadius: '8px' }}
                  itemStyle={{ color: '#e5e7eb' }}
                  labelStyle={{ color: '#8b5cf6', fontWeight: 'bold' }}
                />
                <Legend iconSize={8} iconType="circle" wrapperStyle={{ fontSize: 10, paddingTop: 10 }} />
                <Bar dataKey="DB Timeout" stackId="a" fill="#6366f1" radius={[0, 0, 0, 0]} />
                <Bar dataKey="API Gateway" stackId="a" fill="#f43f5e" radius={[0, 0, 0, 0]} />
                <Bar dataKey="Deployment" stackId="a" fill="#f59e0b" radius={[0, 0, 0, 0]} />
                <Bar dataKey="OOM Leak" stackId="a" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Incident Severity Pie Chart - Occupies 5 columns */}
        <div className="lg:col-span-5 p-5 rounded-2xl glass-panel border border-white/5 space-y-4">
          <h4 className="text-sm font-bold text-gray-200 flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-rose-400" />
            <span>Incident Severity Breakdown</span>
          </h4>
          <div className="h-72 w-full flex flex-col sm:flex-row items-center justify-center gap-4">
            <div className="h-52 w-52">
              <ResponsiveContainer width="100%" height={208} minWidth={0}>
                <PieChart>
                  <Pie
                    data={severityData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={6}
                    dataKey="value"
                  >
                    {severityData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0d101c', borderColor: '#ffffff10', borderRadius: '8px' }}
                    itemStyle={{ color: '#e5e7eb' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            {/* Legend Labels */}
            <div className="space-y-2.5 font-mono text-xs text-gray-400 w-full sm:w-auto">
              {severityData.map((entry, idx) => (
                <div key={entry.name} className="flex items-center gap-2.5">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: entry.color }}></span>
                  <span className="font-semibold text-gray-300">{entry.name}:</span>
                  <span>{entry.value} Cases</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Incident Timeline Chart (Area Chart) - Occupies 6 columns */}
        <div className="lg:col-span-6 p-5 rounded-2xl glass-panel border border-white/5 space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="text-sm font-bold text-gray-200 flex items-center gap-2">
              <Clock className="w-4 h-4 text-violet-400" />
              <span>Weekly Incident Timeline</span>
            </h4>
            <span className="text-[10px] text-gray-500 font-mono">Mon - Sun</span>
          </div>
          <div className="h-64 w-full text-xs font-mono">
            <ResponsiveContainer width="100%" height={256} minWidth={0}>
              <AreaChart data={timelineData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorIncidents" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff08" />
                <XAxis dataKey="day" stroke="#9ca3af" fontSize={10} tickLine={false} />
                <YAxis stroke="#9ca3af" fontSize={10} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0d101c', borderColor: '#ffffff10', borderRadius: '8px' }} />
                <Area type="monotone" dataKey="incidents" stroke="#8b5cf6" strokeWidth={2} fillOpacity={1} fill="url(#colorIncidents)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Score Distribution (Bar Chart) - Occupies 6 columns */}
        <div className="lg:col-span-6 p-5 rounded-2xl glass-panel border border-white/5 space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="text-sm font-bold text-gray-200 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              <span>Risk Score Distribution</span>
            </h4>
            <span className="text-[10px] text-gray-500 font-mono">0 - 100 Index</span>
          </div>
          <div className="h-64 w-full text-xs font-mono">
            <ResponsiveContainer width="100%" height={256} minWidth={0}>
              <BarChart data={riskScoreDistribution} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff08" />
                <XAxis dataKey="range" stroke="#9ca3af" fontSize={10} tickLine={false} />
                <YAxis stroke="#9ca3af" fontSize={10} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0d101c', borderColor: '#ffffff10', borderRadius: '8px' }} />
                <Bar dataKey="count" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Recent Incidents Table */}
      <div className="p-5 rounded-2xl glass-panel border border-white/5 space-y-4">
        <div className="flex justify-between items-center">
          <h4 className="text-sm font-bold text-gray-200">
            Recent Incidents Registry
          </h4>
          <span className="text-xs text-indigo-400">Click row to investigate with AI Agents</span>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-gray-400">
                <th className="pb-3 font-semibold uppercase tracking-wider pl-2">ID</th>
                <th className="pb-3 font-semibold uppercase tracking-wider">Incident Name</th>
                <th className="pb-3 font-semibold uppercase tracking-wider">Severity</th>
                <th className="pb-3 font-semibold uppercase tracking-wider">Status</th>
                <th className="pb-3 font-semibold uppercase tracking-wider">Trigger Source</th>
                <th className="pb-3 font-semibold uppercase tracking-wider pr-2 text-right">Time Detected</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-gray-300">
              {incidents.map((inc) => (
                <tr 
                  key={inc.id}
                  onClick={() => handleIncidentClick(inc.id)}
                  className="hover:bg-white/5 transition-colors cursor-pointer group"
                >
                  <td className="py-3.5 pl-2 font-bold text-indigo-400">{inc.id}</td>
                  <td className="py-3.5 font-sans font-semibold text-gray-200 group-hover:text-indigo-300 transition-colors">
                    {inc.shortName}
                  </td>
                  <td className="py-3.5">
                    <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold ${
                      inc.severity === 'CRITICAL' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                      inc.severity === 'HIGH' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                      'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    }`}>
                      {inc.severity}
                    </span>
                  </td>
                  <td className="py-3.5">
                    <span className="flex items-center gap-1.5">
                      <span className={`w-1.5 h-1.5 rounded-full ${
                        inc.status === 'INVESTIGATING' ? 'bg-amber-500 animate-pulse' : 'bg-emerald-500'
                      }`}></span>
                      <span>{inc.status}</span>
                    </span>
                  </td>
                  <td className="py-3.5 text-gray-400">{inc.category}</td>
                  <td className="py-3.5 pr-2 text-right text-gray-400 flex items-center justify-end gap-2">
                    <span>{inc.time}</span>
                    <ArrowRight className="w-4 h-4 text-gray-500 group-hover:text-indigo-400 group-hover:translate-x-1 transition-all" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};

export default Dashboard;
