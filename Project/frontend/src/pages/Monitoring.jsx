import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { api } from '../services/api';
import { 
  Activity, 
  Server, 
  AlertCircle, 
  CheckCircle, 
  Clock, 
  RefreshCw,
  Database,
  Zap,
  TrendingUp,
  Flame,
  AlertOctagon
} from 'lucide-react';

const Monitoring = () => {
  const navigate = useNavigate();
  const { incidents } = useApp();
  
  // States
  const [logs, setLogs] = useState([]);
  const [failures, setFailures] = useState([]);
  const [systemStatus, setSystemStatus] = useState({
    member1: false,
    member3: false,
    project2: false,
    lastCheck: null
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [lastRefresh, setLastRefresh] = useState(new Date());
  const [loading, setLoading] = useState(true);
  const [injectingFailure, setInjectingFailure] = useState(false);
  const [injectionSuccess, setInjectionSuccess] = useState(null);

  // Fetch all monitoring data
  const fetchMonitoringData = async () => {
    try {
      setLoading(true);

      // Fetch logs from Project 2
      try {
        const logsResponse = await api.getLogs();
        if (logsResponse.success) {
          const logsData = logsResponse.data.logs || [];
          setLogs(logsData.slice(0, 10)); // Latest 10 logs
        }
      } catch (err) {
        console.error('Failed to fetch logs:', err);
      }

      // Fetch failures
      try {
        const failuresResponse = await api.getFailures();
        if (failuresResponse.success) {
          setFailures(failuresResponse.data.failures || []);
        }
      } catch (err) {
        console.error('Failed to fetch failures:', err);
      }

      // Check system health
      const member1Health = await api.healthCheck();
      const member3Health = await api.member3HealthCheck();
      
      let project2Health = false;
      try {
        const project2Response = await api.getProject2Status();
        project2Health = project2Response.success && project2Response.data?.status === 'running';
      } catch (err) {
        project2Health = false;
      }

      setSystemStatus({
        member1: member1Health.success,
        member3: member3Health.success,
        project2: project2Health,
        lastCheck: new Date()
      });

      // Build recent activity from incidents
      const activity = incidents.slice(0, 5).map(inc => ({
        id: inc.id,
        type: 'investigation',
        message: `Investigation ${inc.id}: ${inc.shortName}`,
        status: inc.status,
        time: inc.time
      }));
      setRecentActivity(activity);

      setLastRefresh(new Date());
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch monitoring data:', error);
      setLoading(false);
    }
  };

  // Auto-refresh every 10 seconds
  useEffect(() => {
    fetchMonitoringData();

    if (autoRefresh) {
      const interval = setInterval(() => {
        fetchMonitoringData();
      }, 10000); // 10 seconds

      return () => clearInterval(interval);
    }
  }, [autoRefresh, incidents]);

  const handleManualRefresh = () => {
    fetchMonitoringData();
  };

  const handleInjectFailure = async (failureType) => {
    setInjectingFailure(true);
    setInjectionSuccess(null);

    try {
      const response = await api.injectFailure(failureType);

      if (response.success && response.data?.status === 'injected') {
        setInjectionSuccess({
          type: 'success',
          message: `${failureType.replace('_', ' ').toUpperCase()} injected successfully! Logs generating...`
        });
        
        // Refresh after 3 seconds to show new logs
        setTimeout(() => {
          fetchMonitoringData();
        }, 3000);
      } else {
        setInjectionSuccess({
          type: 'error',
          message: 'Failed to inject failure. Please try again.'
        });
      }
    } catch (error) {
      setInjectionSuccess({
        type: 'error',
        message: `Error: ${error.message}`
      });
    } finally {
      setInjectingFailure(false);
      
      // Clear success message after 10 seconds
      setTimeout(() => {
        setInjectionSuccess(null);
      }, 10000);
    }
  };

  const getStatusColor = (healthy) => {
    return healthy ? 'text-emerald-400' : 'text-rose-400';
  };

  const getStatusBg = (healthy) => {
    return healthy ? 'bg-emerald-500/10 border-emerald-500/20' : 'bg-rose-500/10 border-rose-500/20';
  };

  const formatTime = (timestamp) => {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  const getLogLevelColor = (level) => {
    switch (level?.toUpperCase()) {
      case 'ERROR':
        return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
      case 'WARN':
      case 'WARNING':
        return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      case 'INFO':
        return 'text-blue-400 bg-blue-500/10 border-blue-500/20';
      default:
        return 'text-gray-400 bg-gray-500/10 border-gray-500/20';
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Title Bar */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 p-6 rounded-2xl glass-panel border border-white/5 shadow-glass">
        <div>
          <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider">
            <Activity className="w-4 h-4 animate-pulse" />
            <span>Real-Time Monitoring</span>
          </div>
          <h2 className="text-2xl font-extrabold text-gray-100 mt-1">
            System Health Dashboard
          </h2>
          <p className="text-sm text-gray-400 mt-1">
            Live monitoring of all SmartOps components and recent activity
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-xs text-gray-300 font-mono">
            <Clock className="w-3.5 h-3.5" />
            <span>Last refresh: {formatTime(lastRefresh)}</span>
          </div>

          <button
            onClick={handleManualRefresh}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 text-xs font-bold rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white shadow-glow-indigo transition-all cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh Now</span>
          </button>

          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
              autoRefresh 
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white' 
                : 'bg-gray-600 hover:bg-gray-500 text-white'
            }`}
          >
            <Zap className="w-3.5 h-3.5" />
            <span>Auto: {autoRefresh ? 'ON' : 'OFF'}</span>
          </button>
        </div>
      </div>

      {/* System Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        {/* Member 1 Status */}
        <div className={`p-5 rounded-2xl glass-panel border shadow-glass ${getStatusBg(systemStatus.member1)}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Server className={`w-8 h-8 ${getStatusColor(systemStatus.member1)}`} />
              <div>
                <h3 className="text-sm font-bold text-gray-200">Member 1</h3>
                <p className="text-xs text-gray-400 font-mono">Investigation Backend</p>
              </div>
            </div>
            {systemStatus.member1 ? (
              <CheckCircle className="w-5 h-5 text-emerald-400" />
            ) : (
              <AlertCircle className="w-5 h-5 text-rose-400" />
            )}
          </div>
          <div className="mt-3 flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${systemStatus.member1 ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`}></span>
            <span className={`text-xs font-semibold font-mono ${getStatusColor(systemStatus.member1)}`}>
              {systemStatus.member1 ? 'HEALTHY' : 'OFFLINE'}
            </span>
          </div>
          <p className="text-xs text-gray-500 mt-2 font-mono">Port: 8000</p>
        </div>

        {/* Member 3 Status */}
        <div className={`p-5 rounded-2xl glass-panel border shadow-glass ${getStatusBg(systemStatus.member3)}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Database className={`w-8 h-8 ${getStatusColor(systemStatus.member3)}`} />
              <div>
                <h3 className="text-sm font-bold text-gray-200">Member 3</h3>
                <p className="text-xs text-gray-400 font-mono">AI/RCA Engine</p>
              </div>
            </div>
            {systemStatus.member3 ? (
              <CheckCircle className="w-5 h-5 text-emerald-400" />
            ) : (
              <AlertCircle className="w-5 h-5 text-rose-400" />
            )}
          </div>
          <div className="mt-3 flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${systemStatus.member3 ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`}></span>
            <span className={`text-xs font-semibold font-mono ${getStatusColor(systemStatus.member3)}`}>
              {systemStatus.member3 ? 'HEALTHY' : 'OFFLINE'}
            </span>
          </div>
          <p className="text-xs text-gray-500 mt-2 font-mono">Port: 8002</p>
        </div>

        {/* Project 2 Status */}
        <div className={`p-5 rounded-2xl glass-panel border shadow-glass ${getStatusBg(systemStatus.project2)}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <TrendingUp className={`w-8 h-8 ${getStatusColor(systemStatus.project2)}`} />
              <div>
                <h3 className="text-sm font-bold text-gray-200">Project 2</h3>
                <p className="text-xs text-gray-400 font-mono">Chaos Demo Platform</p>
              </div>
            </div>
            {systemStatus.project2 ? (
              <CheckCircle className="w-5 h-5 text-emerald-400" />
            ) : (
              <AlertCircle className="w-5 h-5 text-rose-400" />
            )}
          </div>
          <div className="mt-3 flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${systemStatus.project2 ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`}></span>
            <span className={`text-xs font-semibold font-mono ${getStatusColor(systemStatus.project2)}`}>
              {systemStatus.project2 ? 'RUNNING' : 'UNAVAILABLE'}
            </span>
          </div>
          <p className="text-xs text-gray-500 mt-2 font-mono">Deployed</p>
        </div>

      </div>

      {/* Failure Injection Panel - NEW */}
      <div className="p-6 rounded-2xl glass-panel border border-rose-500/20 shadow-glass bg-rose-500/5">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-lg bg-rose-500/10">
            <Flame className="w-5 h-5 text-rose-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-100">Chaos Engineering - Failure Injection</h3>
            <p className="text-xs text-gray-400 mt-0.5">Inject failures into Project 2 to test incident response</p>
          </div>
        </div>

        {/* Success/Error Message */}
        {injectionSuccess && (
          <div className={`mb-4 p-3 rounded-lg border ${
            injectionSuccess.type === 'success' 
              ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' 
              : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
          }`}>
            <div className="flex items-center gap-2">
              {injectionSuccess.type === 'success' ? (
                <CheckCircle className="w-4 h-4" />
              ) : (
                <AlertOctagon className="w-4 h-4" />
              )}
              <span className="text-sm font-medium">{injectionSuccess.message}</span>
            </div>
          </div>
        )}

        {/* Failure Type Buttons */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          <button
            onClick={() => handleInjectFailure('db_timeout')}
            disabled={injectingFailure}
            className="flex flex-col items-center gap-2 p-4 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 hover:border-rose-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <Database className="w-6 h-6 text-rose-400 group-hover:scale-110 transition-transform" />
            <span className="text-xs font-bold text-gray-200">DB Timeout</span>
          </button>

          <button
            onClick={() => handleInjectFailure('memory_leak')}
            disabled={injectingFailure}
            className="flex flex-col items-center gap-2 p-4 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 hover:border-amber-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <Zap className="w-6 h-6 text-amber-400 group-hover:scale-110 transition-transform" />
            <span className="text-xs font-bold text-gray-200">Memory Leak</span>
          </button>

          <button
            onClick={() => handleInjectFailure('cpu_spike')}
            disabled={injectingFailure}
            className="flex flex-col items-center gap-2 p-4 rounded-lg bg-orange-500/10 hover:bg-orange-500/20 border border-orange-500/30 hover:border-orange-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <Activity className="w-6 h-6 text-orange-400 group-hover:scale-110 transition-transform" />
            <span className="text-xs font-bold text-gray-200">CPU Spike</span>
          </button>

          <button
            onClick={() => handleInjectFailure('missing_env')}
            disabled={injectingFailure}
            className="flex flex-col items-center gap-2 p-4 rounded-lg bg-violet-500/10 hover:bg-violet-500/20 border border-violet-500/30 hover:border-violet-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <AlertCircle className="w-6 h-6 text-violet-400 group-hover:scale-110 transition-transform" />
            <span className="text-xs font-bold text-gray-200">Missing ENV</span>
          </button>

          <button
            onClick={() => handleInjectFailure('gateway_failure')}
            disabled={injectingFailure}
            className="flex flex-col items-center gap-2 p-4 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 hover:border-indigo-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <Server className="w-6 h-6 text-indigo-400 group-hover:scale-110 transition-transform" />
            <span className="text-xs font-bold text-gray-200">Gateway Fail</span>
          </button>

          <button
            onClick={() => handleInjectFailure('null_pointer')}
            disabled={injectingFailure}
            className="flex flex-col items-center gap-2 p-4 rounded-lg bg-pink-500/10 hover:bg-pink-500/20 border border-pink-500/30 hover:border-pink-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <AlertOctagon className="w-6 h-6 text-pink-400 group-hover:scale-110 transition-transform" />
            <span className="text-xs font-bold text-gray-200">Null Pointer</span>
          </button>
        </div>

        <p className="text-xs text-gray-500 mt-4 text-center font-mono">
          {injectingFailure ? '⏳ Injecting failure...' : 'Click a failure type to inject into Project 2 (Duration: 5 minutes)'}
        </p>
      </div>

      {/* Latest Logs and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Latest Logs */}
        <div className="p-5 rounded-2xl glass-panel border border-white/5 shadow-glass space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-gray-200 flex items-center gap-2">
              <Activity className="w-4 h-4 text-blue-400" />
              <span>Latest Logs</span>
            </h4>
            <span className="text-xs text-gray-500 font-mono">From Project 2</span>
          </div>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {logs.length === 0 ? (
              <div className="text-center py-8 text-gray-500 text-xs">
                No logs available
              </div>
            ) : (
              logs.map((log, idx) => (
                <div key={idx} className="p-3 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${getLogLevelColor(log.level)}`}>
                          {log.level || 'INFO'}
                        </span>
                        <span className="text-[10px] text-gray-500 font-mono">{log.source || 'system'}</span>
                      </div>
                      <p className="text-xs text-gray-300 font-mono break-words">
                        {log.message || 'No message'}
                      </p>
                    </div>
                    <span className="text-[10px] text-gray-500 whitespace-nowrap">
                      {formatTime(log.timestamp)}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="p-5 rounded-2xl glass-panel border border-white/5 shadow-glass space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-gray-200 flex items-center gap-2">
              <Clock className="w-4 h-4 text-violet-400" />
              <span>Recent Activity</span>
            </h4>
            <span className="text-xs text-gray-500 font-mono">Investigations</span>
          </div>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {recentActivity.length === 0 ? (
              <div className="text-center py-8 text-gray-500 text-xs">
                No recent activity
              </div>
            ) : (
              recentActivity.map((activity, idx) => (
                <div 
                  key={idx} 
                  className="p-3 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-colors cursor-pointer group"
                  onClick={() => navigate(`/results?id=${activity.id}`)}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`w-1.5 h-1.5 rounded-full ${
                          activity.status === 'INVESTIGATING' ? 'bg-amber-500 animate-pulse' : 'bg-emerald-500'
                        }`}></span>
                        <span className="text-xs font-semibold text-gray-300 group-hover:text-indigo-300 transition-colors">
                          {activity.message}
                        </span>
                      </div>
                      <p className="text-[10px] text-gray-500 font-mono">
                        Status: {activity.status}
                      </p>
                    </div>
                    <span className="text-[10px] text-gray-500">
                      {activity.time}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>

      {/* Failure Events */}
      {failures.length > 0 && (
        <div className="p-5 rounded-2xl glass-panel border border-rose-500/20 shadow-glass space-y-4 bg-rose-500/5">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-gray-200 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-400" />
              <span>Active Failure Events</span>
            </h4>
            <span className="text-xs text-rose-400 font-mono">{failures.length} failures</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {failures.map((failure, idx) => (
              <div key={idx} className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <AlertCircle className="w-4 h-4 text-rose-400" />
                  <span className="text-xs font-bold text-rose-300">{failure.type || 'Unknown'}</span>
                </div>
                <p className="text-xs text-gray-400 font-mono">
                  {failure.message || 'Failure detected'}
                </p>
                <p className="text-[10px] text-gray-500 mt-2">
                  {formatTime(failure.timestamp)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* System Info Footer */}
      <div className="p-4 rounded-2xl glass-panel border border-white/5 shadow-glass">
        <div className="flex flex-wrap items-center justify-between gap-4 text-xs text-gray-400 font-mono">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>Auto-refresh: {autoRefresh ? 'Enabled (10s)' : 'Disabled'}</span>
          </div>
          <div>Last health check: {systemStatus.lastCheck ? formatTime(systemStatus.lastCheck) : 'Never'}</div>
          <div>Total Incidents: {incidents.length}</div>
        </div>
      </div>

    </div>
  );
};

export default Monitoring;
