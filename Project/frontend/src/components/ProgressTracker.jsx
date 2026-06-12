import React, { useState, useEffect } from 'react';
import { Loader2, CheckCircle2, Circle, AlertCircle } from 'lucide-react';

const ProgressTracker = ({ onComplete }) => {
  const [progress, setProgress] = useState(0);
  
  // Status states: 'pending', 'running', 'completed'
  const [agents, setAgents] = useState({
    github: { status: 'pending', label: 'GitHub Agent', desc: 'Awaiting initialization...' },
    log: { status: 'pending', label: 'Log Agent', desc: 'Awaiting log file...' },
    investigation: { status: 'pending', label: 'Investigation Agent', desc: 'Awaiting correlation patterns...' },
    groq: { status: 'pending', label: 'Groq Agent', desc: 'Awaiting SRE report generation...' }
  });

  useEffect(() => {
    let active = true;

    const runSequence = async () => {
      // Step 1: GitHub Agent (0s - 1.5s)
      if (!active) return;
      setAgents(prev => ({
        ...prev,
        github: { status: 'running', label: 'GitHub Agent', desc: 'Authenticating repository URL and parsing git ref logs...' }
      }));
      setProgress(15);
      await new Promise(r => setTimeout(r, 1200));

      if (!active) return;
      setAgents(prev => ({
        ...prev,
        github: { status: 'completed', label: 'GitHub Agent', desc: 'Successfully connected. Pulled recent commit history (v2.4.1).' }
      }));
      setProgress(30);

      // Step 2: Log Agent (1.5s - 3s)
      if (!active) return;
      setAgents(prev => ({
        ...prev,
        log: { status: 'running', label: 'Log Agent', desc: 'Ingesting file streams and parsing log stack signatures...' }
      }));
      setProgress(45);
      await new Promise(r => setTimeout(r, 1200));

      if (!active) return;
      setAgents(prev => ({
        ...prev,
        log: { status: 'completed', label: 'Log Agent', desc: 'Identified PostgreSQL and Gateway connection pool exceptions.' }
      }));
      setProgress(60);

      // Step 3: Investigation Agent (3s - 4.5s)
      if (!active) return;
      setAgents(prev => ({
        ...prev,
        investigation: { status: 'running', label: 'Investigation Agent', desc: 'Cross-correlating logs against git diff modifications...' }
      }));
      setProgress(75);
      await new Promise(r => setTimeout(r, 1200));

      if (!active) return;
      setAgents(prev => ({
        ...prev,
        investigation: { status: 'completed', label: 'Investigation Agent', desc: 'Root cause identified: unindexed query N+1 loop in OrderService.' }
      }));
      setProgress(90);

      // Step 4: Groq Agent (4.5s - 5.5s)
      if (!active) return;
      setAgents(prev => ({
        ...prev,
        groq: { status: 'running', label: 'Groq Agent', desc: 'Compiling SRE recommendations and rendering RCA markdown reports...' }
      }));
      setProgress(95);
      await new Promise(r => setTimeout(r, 1000));

      if (!active) return;
      setAgents(prev => ({
        ...prev,
        groq: { status: 'completed', label: 'Groq Agent', desc: 'RCA PDF compilation and AI Recommendations ready.' }
      }));
      setProgress(100);
      
      await new Promise(r => setTimeout(r, 600));
      if (active) {
        onComplete();
      }
    };

    runSequence();

    return () => {
      active = false;
    };
  }, []);

  const renderAgentRow = (agentKey, agent) => {
    const { status, label, desc } = agent;
    return (
      <div 
        key={agentKey} 
        className={`flex items-start gap-4 p-4 rounded-xl border transition-all duration-200 ${
          status === 'running' 
            ? 'bg-indigo-500/5 border-indigo-500/25 shadow-glow-indigo' 
            : status === 'completed'
              ? 'bg-emerald-500/5 border-emerald-500/10'
              : 'bg-white/5 border-white/5 opacity-55'
        }`}
      >
        <div className="shrink-0 mt-0.5">
          {status === 'running' && <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />}
          {status === 'completed' && <CheckCircle2 className="w-5 h-5 text-emerald-400" />}
          {status === 'pending' && <Circle className="w-5 h-5 text-gray-500" />}
        </div>
        <div className="space-y-0.5 text-left">
          <span className={`text-xs font-bold font-mono tracking-wide ${
            status === 'running' ? 'text-indigo-300' : status === 'completed' ? 'text-emerald-400' : 'text-gray-400'
          }`}>
            {label}
          </span>
          <p className="text-xs text-gray-300 font-sans leading-relaxed">{desc}</p>
        </div>
      </div>
    );
  };

  return (
    <div className="p-8 rounded-2xl glass-panel border border-white/5 shadow-glass text-center space-y-8 max-w-xl mx-auto">
      
      {/* Visual Loader Circle */}
      <div className="flex flex-col items-center justify-center space-y-4">
        <div className="relative flex items-center justify-center w-20 h-20">
          <Loader2 className="w-16 h-16 text-indigo-500 animate-spin" />
          <span className="absolute text-xs font-bold font-mono text-indigo-300">{progress}%</span>
        </div>
        <div className="space-y-1">
          <h4 className="text-md font-bold text-gray-100">Running Multi-Agent Diagnostic Models</h4>
          <p className="text-xs text-gray-400">Verifying repository logs, telemetry sequences, and diff structures</p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
        <div 
          className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 transition-all duration-300 rounded-full"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Agents Checklist Stack */}
      <div className="space-y-3">
        {Object.entries(agents).map(([key, val]) => renderAgentRow(key, val))}
      </div>

    </div>
  );
};

export default ProgressTracker;
