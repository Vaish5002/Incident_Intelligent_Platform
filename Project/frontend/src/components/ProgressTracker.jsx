import React, { useState, useEffect } from 'react';
import { Loader2, CheckCircle2, Circle, AlertCircle, Zap, GitBranch, FileText, Brain, Shield, TrendingUp } from 'lucide-react';

const ProgressTracker = ({ onComplete }) => {
  const [progress, setProgress] = useState(0);
  const [currentPhase, setCurrentPhase] = useState('');
  const [detailedStatus, setDetailedStatus] = useState('');
  const [findings, setFindings] = useState([]);
  
  // Status states: 'pending', 'running', 'completed'
  const [agents, setAgents] = useState({
    github: { status: 'pending', label: 'GitHub Agent', desc: 'Awaiting initialization...', icon: GitBranch },
    log: { status: 'pending', label: 'Log Agent', desc: 'Awaiting log file...', icon: FileText },
    correlation: { status: 'pending', label: 'Correlation Engine', desc: 'Awaiting pattern matching...', icon: TrendingUp },
    investigation: { status: 'pending', label: 'Investigation Agent', desc: 'Awaiting analysis...', icon: Brain },
    risk: { status: 'pending', label: 'Risk Scoring', desc: 'Awaiting risk assessment...', icon: Shield },
    groq: { status: 'pending', label: 'AI Report Generator', desc: 'Awaiting SRE report generation...', icon: Zap }
  });

  useEffect(() => {
    let active = true;

    const runSequence = async () => {
      // Phase 1: GitHub Agent (0s - 2.5s)
      if (!active) return;
      setCurrentPhase('Connecting to Repository');
      setDetailedStatus('Authenticating with GitHub API...');
      setAgents(prev => ({
        ...prev,
        github: { ...prev.github, status: 'running', desc: 'Authenticating repository URL and parsing git ref logs...' }
      }));
      setProgress(5);
      await new Promise(r => setTimeout(r, 600));

      if (!active) return;
      setDetailedStatus('Fetching recent commits (last 30 days)...');
      setProgress(10);
      await new Promise(r => setTimeout(r, 500));

      if (!active) return;
      setDetailedStatus('Analyzing commit metadata and file changes...');
      setProgress(15);
      await new Promise(r => setTimeout(r, 700));

      if (!active) return;
      setFindings(prev => [...prev, '✓ Analyzing commit history in repository']);
      setDetailedStatus('Identifying risky code changes...');
      setProgress(18);
      await new Promise(r => setTimeout(r, 600));

      if (!active) return;
      setFindings(prev => [...prev, '⚠️ Scanning for high-risk commits affecting critical components']);
      setAgents(prev => ({
        ...prev,
        github: { ...prev.github, status: 'completed', desc: 'Successfully analyzed commit history and identified code changes.' }
      }));
      setProgress(22);

      // Phase 2: Log Agent (2.5s - 5.5s)
      if (!active) return;
      setCurrentPhase('Processing Runtime Logs');
      setDetailedStatus('Ingesting application logs...');
      setAgents(prev => ({
        ...prev,
        log: { ...prev.log, status: 'running', desc: 'Parsing log streams and extracting error signatures...' }
      }));
      setProgress(28);
      await new Promise(r => setTimeout(r, 700));

      if (!active) return;
      setDetailedStatus('Detecting error patterns and anomalies...');
      setProgress(35);
      await new Promise(r => setTimeout(r, 600));

      if (!active) return;
      setFindings(prev => [...prev, '✓ Processing application error logs']);
      setDetailedStatus('Classifying failure signatures...');
      setProgress(40);
      await new Promise(r => setTimeout(r, 700));

      if (!active) return;
      setFindings(prev => [...prev, '🔍 Analyzing error patterns and failure signatures']);
      setAgents(prev => ({
        ...prev,
        log: { ...prev.log, status: 'completed', desc: 'Log analysis complete with error patterns and failure signatures identified.' }
      }));
      setProgress(45);

      // Phase 3: Correlation Engine (5.5s - 7.5s)
      if (!active) return;
      setCurrentPhase('Correlating Events');
      setDetailedStatus('Matching logs with code changes...');
      setAgents(prev => ({
        ...prev,
        correlation: { ...prev.correlation, status: 'running', desc: 'Cross-correlating timestamps and execution traces...' }
      }));
      setProgress(52);
      await new Promise(r => setTimeout(r, 600));

      if (!active) return;
      setDetailedStatus('Building event timeline...');
      setProgress(58);
      await new Promise(r => setTimeout(r, 700));

      if (!active) return;
      setFindings(prev => [...prev, '⏱️ Building event timeline from deployment to incident']);
      setAgents(prev => ({
        ...prev,
        correlation: { ...prev.correlation, status: 'completed', desc: 'Successfully correlated code changes with error patterns and timeline.' }
      }));
      setProgress(62);

      // Phase 4: Investigation Agent (7.5s - 9.5s)
      if (!active) return;
      setCurrentPhase('Root Cause Analysis');
      setDetailedStatus('Analyzing code complexity and database queries...');
      setAgents(prev => ({
        ...prev,
        investigation: { ...prev.investigation, status: 'running', desc: 'Executing deep code analysis and pattern recognition...' }
      }));
      setProgress(68);
      await new Promise(r => setTimeout(r, 800));

      if (!active) return;
      setDetailedStatus('Comparing with historical incident patterns...');
      setProgress(73);
      await new Promise(r => setTimeout(r, 600));

      if (!active) return;
      setFindings(prev => [...prev, '🎯 Identifying root cause from code and log correlation']);
      setDetailedStatus('Validating root cause hypothesis...');
      setProgress(78);
      await new Promise(r => setTimeout(r, 700));

      if (!active) return;
      setFindings(prev => [...prev, '✓ Comparing with historical incident patterns']);
      setAgents(prev => ({
        ...prev,
        investigation: { ...prev.investigation, status: 'completed', desc: 'Root cause analysis complete with validated hypothesis and evidence.' }
      }));
      setProgress(82);

      // Phase 5: Risk Scoring (9.5s - 10.5s)
      if (!active) return;
      setCurrentPhase('Risk Assessment');
      setDetailedStatus('Calculating severity and business impact...');
      setAgents(prev => ({
        ...prev,
        risk: { ...prev.risk, status: 'running', desc: 'Computing risk score based on multiple factors...' }
      }));
      setProgress(86);
      await new Promise(r => setTimeout(r, 700));

      if (!active) return;
      setFindings(prev => [...prev, '📊 Calculating risk score and severity level']);
      setDetailedStatus('Generating impact assessment...');
      setProgress(90);
      await new Promise(r => setTimeout(r, 500));

      if (!active) return;
      setAgents(prev => ({
        ...prev,
        risk: { ...prev.risk, status: 'completed', desc: 'Risk assessment complete with severity classification and impact analysis.' }
      }));
      setProgress(93);

      // Phase 6: AI Report Generator (10.5s - 12s)
      if (!active) return;
      setCurrentPhase('Generating Report');
      setDetailedStatus('AI synthesizing findings and recommendations...');
      setAgents(prev => ({
        ...prev,
        groq: { ...prev.groq, status: 'running', desc: 'Generating RCA report with prioritized action items...' }
      }));
      setProgress(96);
      await new Promise(r => setTimeout(r, 800));

      if (!active) return;
      setDetailedStatus('Compiling PDF and executive summary...');
      setProgress(98);
      await new Promise(r => setTimeout(r, 600));

      if (!active) return;
      setFindings(prev => [...prev, '📄 Generating comprehensive RCA report with recommendations']);
      setAgents(prev => ({
        ...prev,
        groq: { ...prev.groq, status: 'completed', desc: 'Complete investigation report ready with PDF export.' }
      }));
      setProgress(100);
      setCurrentPhase('Investigation Complete');
      setDetailedStatus('Redirecting to results...');
      
      await new Promise(r => setTimeout(r, 800));
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
    const { status, label, desc, icon: Icon } = agent;
    return (
      <div 
        key={agentKey} 
        className={`flex items-start gap-4 p-4 rounded-xl border transition-all duration-300 ${
          status === 'running' 
            ? 'bg-indigo-500/10 border-indigo-500/30 shadow-[0_0_20px_rgba(99,102,241,0.15)]' 
            : status === 'completed'
              ? 'bg-emerald-500/5 border-emerald-500/20'
              : 'bg-white/5 border-white/5 opacity-50'
        }`}
      >
        <div className="shrink-0 mt-0.5">
          {status === 'running' && (
            <div className="relative">
              <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
              <div className="absolute inset-0 w-5 h-5 rounded-full bg-indigo-500/20 animate-ping" />
            </div>
          )}
          {status === 'completed' && <CheckCircle2 className="w-5 h-5 text-emerald-400" />}
          {status === 'pending' && <Circle className="w-5 h-5 text-gray-600" />}
        </div>
        <div className="flex-1 space-y-1 text-left">
          <div className="flex items-center gap-2">
            <Icon className={`w-4 h-4 ${
              status === 'running' ? 'text-indigo-400' : 
              status === 'completed' ? 'text-emerald-400' : 
              'text-gray-600'
            }`} />
            <span className={`text-xs font-bold font-mono tracking-wide ${
              status === 'running' ? 'text-indigo-300' : 
              status === 'completed' ? 'text-emerald-300' : 
              'text-gray-500'
            }`}>
              {label}
            </span>
          </div>
          <p className={`text-xs font-sans leading-relaxed transition-colors ${
            status === 'running' ? 'text-gray-200' : 'text-gray-400'
          }`}>{desc}</p>
        </div>
      </div>
    );
  };

  return (
    <div className="p-8 rounded-2xl glass-panel border border-white/5 shadow-glass space-y-6 max-w-4xl mx-auto">
      
      {/* Header with Phase Indicator */}
      <div className="flex flex-col items-center justify-center space-y-3 pb-4 border-b border-white/10">
        <div className="relative flex items-center justify-center w-24 h-24">
          <div className="absolute inset-0 rounded-full bg-indigo-500/10 animate-pulse" />
          <div className="absolute inset-2 rounded-full border-2 border-indigo-500/20 border-dashed animate-spin-slow" />
          <Loader2 className="w-14 h-14 text-indigo-500 animate-spin relative z-10" />
          <span className="absolute text-sm font-bold font-mono text-indigo-300 z-20">{progress}%</span>
        </div>
        <div className="space-y-1.5 text-center">
          <h4 className="text-lg font-bold text-gray-100 flex items-center justify-center gap-2">
            <Zap className="w-5 h-5 text-indigo-400" />
            {currentPhase || 'Initializing Multi-Agent System'}
          </h4>
          <p className="text-xs text-indigo-300 font-mono">{detailedStatus}</p>
        </div>
      </div>

      {/* Enhanced Progress Bar with Segments */}
      <div className="space-y-2">
        <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden relative">
          <div 
            className="h-full bg-gradient-to-r from-indigo-600 via-purple-500 to-pink-500 transition-all duration-500 ease-out rounded-full relative"
            style={{ width: `${progress}%` }}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
          </div>
        </div>
        <div className="flex justify-between text-[10px] text-gray-500 font-mono">
          <span>GitHub</span>
          <span>Logs</span>
          <span>Correlate</span>
          <span>Analyze</span>
          <span>Risk</span>
          <span>Report</span>
        </div>
      </div>

      {/* Real-time Findings Feed */}
      {findings.length > 0 && (
        <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-indigo-400" />
            <span className="text-xs font-bold text-gray-300">Live Findings</span>
          </div>
          <div className="space-y-1.5 max-h-32 overflow-y-auto custom-scrollbar">
            {findings.map((finding, idx) => (
              <div 
                key={idx} 
                className="text-xs text-gray-300 font-mono py-1.5 px-3 bg-white/5 rounded-lg border border-white/5 animate-slideInLeft"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                {finding}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Agents Grid - 2 columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {Object.entries(agents).map(([key, val]) => renderAgentRow(key, val))}
      </div>

      {/* Bottom Status */}
      <div className="pt-4 border-t border-white/10 text-center">
        <p className="text-xs text-gray-500">
          {progress < 100 
            ? 'Investigation in progress... Do not close this window.' 
            : 'Investigation complete! Preparing results...'}
        </p>
      </div>

    </div>
  );
};

export default ProgressTracker;
