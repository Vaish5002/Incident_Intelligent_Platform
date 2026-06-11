import React from 'react';
import { useApp } from '../context/AppContext';
import { 
  Cpu, 
  Terminal, 
  Clock, 
  GitBranch, 
  AlertTriangle, 
  ShieldAlert,
  ListChecks,
  Code,
  User,
  Activity
} from 'lucide-react';

const Analysis = () => {
  const { incidents, activeIncidentId, setActiveIncidentId, activeIncident } = useApp();

  if (!activeIncident) {
    return (
      <div className="p-8 text-center text-gray-400 font-mono">
        Loading active incident analysis context...
      </div>
    );
  }

  // Helper to colorize git diff content lines
  const renderDiffLine = (line, index) => {
    if (line.startsWith('+')) {
      return (
        <div key={index} className="text-emerald-400 bg-emerald-500/10 px-2 py-0.5 font-mono text-xs border-l-2 border-emerald-500">
          {line}
        </div>
      );
    } else if (line.startsWith('-')) {
      return (
        <div key={index} className="text-rose-400 bg-rose-500/10 px-2 py-0.5 font-mono text-xs border-l-2 border-rose-500">
          {line}
        </div>
      );
    } else if (line.startsWith('@@') || line.startsWith('diff') || line.startsWith('index')) {
      return (
        <div key={index} className="text-indigo-400 bg-indigo-500/5 px-2 py-0.5 font-mono text-xs font-semibold">
          {line}
        </div>
      );
    }
    return (
      <div key={index} className="text-gray-400 px-2 py-0.5 font-mono text-xs">
        {line}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      
      {/* Header Selector bar */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 p-5 rounded-2xl glass-panel border border-white/5 shadow-glass">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 font-bold text-xs uppercase tracking-wider">
            <Cpu className="w-4 h-4" />
            <span>Agentic Investigation Workbench</span>
          </div>
          <h2 className="text-2xl font-extrabold text-gray-100 mt-1">
            Analyzing {activeIncident.id}
          </h2>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <label className="text-xs text-gray-400 font-mono">Switch Target:</label>
          <select
            value={activeIncidentId}
            onChange={(e) => setActiveIncidentId(e.target.value)}
            className="pl-3 pr-8 py-2 text-xs font-mono font-bold rounded-lg bg-white/5 border border-white/10 text-gray-200 outline-none cursor-pointer appearance-none min-w-[220px]"
          >
            {incidents.map((inc) => (
              <option key={inc.id} value={inc.id} className="bg-bg-darker text-gray-200">
                {inc.id}: {inc.shortName}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Grid Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Hand Agents (Log & Git) - 8 columns */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* Agent A: Log Analysis Agent */}
          <div className="rounded-2xl glass-panel border border-white/5 shadow-glass overflow-hidden">
            <div className="flex items-center justify-between px-5 py-4 bg-white/5 border-b border-white/5">
              <div className="flex items-center gap-2.5">
                <div className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400">
                  <Terminal className="w-4.5 h-4.5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-gray-200">Log Analysis Agent</h3>
                  <p className="text-[10px] text-gray-400">Parsed {activeIncident.logAnalysis.errorCount} system errors</p>
                </div>
              </div>
              <span className="text-[9px] font-mono px-2 py-0.5 bg-indigo-500/10 text-indigo-300 rounded-full border border-indigo-500/20 font-bold uppercase animate-pulse-slow">
                COMPLETED
              </span>
            </div>
            
            <div className="p-5 space-y-4">
              <div className="space-y-1">
                <span className="text-[10px] text-gray-400 font-bold uppercase tracking-wider font-mono">Identified Root Cause</span>
                <p className="text-sm text-gray-200 leading-relaxed bg-indigo-500/5 p-3 rounded-lg border border-indigo-500/10 font-medium">
                  {activeIncident.logAnalysis.rootCause}
                </p>
              </div>

              {/* Error Patterns list */}
              <div className="space-y-2">
                <span className="text-[10px] text-gray-400 font-bold uppercase tracking-wider font-mono">Extracted Error Signature Patterns</span>
                <div className="flex flex-col gap-1.5">
                  {activeIncident.logAnalysis.errorPatterns.map((pat, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-xs font-mono text-rose-300 bg-rose-500/5 p-2 rounded-lg border border-rose-500/10">
                      <ShieldAlert className="w-4 h-4 shrink-0 text-rose-400" />
                      <span className="truncate">{pat}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Raw Logs terminal */}
              <div className="space-y-1.5 pt-2">
                <span className="text-[10px] text-gray-400 font-bold uppercase tracking-wider font-mono">Agent Diagnostics Terminal Stream</span>
                <div className="bg-bg-darker border border-white/5 rounded-lg p-4 font-mono text-xs text-gray-300 overflow-x-auto h-48 scrollbar">
                  <pre className="whitespace-pre">{activeIncident.logAnalysis.rawLogs}</pre>
                </div>
              </div>
            </div>
          </div>

          {/* Agent C: Git Analysis Agent */}
          <div className="rounded-2xl glass-panel border border-white/5 shadow-glass overflow-hidden">
            <div className="flex items-center justify-between px-5 py-4 bg-white/5 border-b border-white/5">
              <div className="flex items-center gap-2.5">
                <div className="p-1.5 rounded-lg bg-violet-500/10 text-violet-400">
                  <GitBranch className="w-4.5 h-4.5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-gray-200">Git Analysis Agent</h3>
                  <p className="text-[10px] text-gray-400">Analyzing commits against telemetry timelines</p>
                </div>
              </div>
              <span className="text-[9px] font-mono px-2 py-0.5 bg-violet-500/10 text-violet-300 rounded-full border border-violet-500/20 font-bold uppercase">
                RESOLVED
              </span>
            </div>

            <div className="p-5 space-y-4">
              {activeIncident.gitAnalysis.riskyCodeChanges.length > 0 ? (
                <>
                  <div className="flex justify-between items-center bg-white/5 p-3 rounded-lg border border-white/5">
                    <div>
                      <div className="text-[10px] text-gray-500 font-mono uppercase font-bold">Risky Commit Target</div>
                      <div className="text-xs font-semibold text-gray-200 mt-0.5">
                        Hash: <span className="font-mono text-violet-400">{activeIncident.gitAnalysis.commitHash}</span> 
                        <span className="mx-2 text-gray-500">|</span> 
                        Author: <span className="font-sans text-gray-300 font-normal">{activeIncident.gitAnalysis.author}</span>
                      </div>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 border border-rose-500/25 text-rose-400 uppercase">
                      ALERT TRIGGER
                    </span>
                  </div>

                  {/* Code changes summary */}
                  <div className="space-y-2">
                    <span className="text-[10px] text-gray-400 font-bold uppercase tracking-wider font-mono">Code Modification Risk Assessment</span>
                    {activeIncident.gitAnalysis.riskyCodeChanges.map((change, idx) => (
                      <div key={idx} className="p-3 bg-white/5 rounded-lg border border-white/5 space-y-1">
                        <div className="flex justify-between text-[11px] font-mono text-indigo-400 font-bold">
                          <span>File: {change.file} (Line {change.line})</span>
                          <span className="text-rose-400">{change.severity} Risk</span>
                        </div>
                        <p className="text-xs text-gray-300 leading-normal">{change.change}</p>
                      </div>
                    ))}
                  </div>

                  {/* Git Diff Display */}
                  <div className="space-y-1.5">
                    <span className="text-[10px] text-gray-400 font-bold uppercase tracking-wider font-mono">Risky Diff Ingest Payload</span>
                    <div className="bg-bg-darker border border-white/5 rounded-lg p-3 overflow-x-auto max-h-60 scrollbar flex flex-col gap-0.5 font-mono leading-relaxed">
                      {activeIncident.gitAnalysis.diff.split('\n').map((line, idx) => renderDiffLine(line, idx))}
                    </div>
                  </div>
                </>
              ) : (
                <div className="flex flex-col items-center justify-center p-8 text-center text-gray-400 space-y-2">
                  <Code className="w-10 h-10 text-gray-500" />
                  <p className="text-xs font-mono">No repository modifications identified.</p>
                  <p className="text-[10px] text-gray-500">This incident appears to be associated with an external server outage.</p>
                </div>
              )}
            </div>
          </div>

        </div>

        {/* Right Hand Agents (Risk, Timeline, Recommendations) - 4 columns */}
        <div className="lg:col-span-4 space-y-6">
          
          {/* Agent D: Risk Assessment Agent */}
          <div className="p-5 rounded-2xl glass-panel border border-white/5 shadow-glass space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-white/5">
              <h3 className="text-sm font-bold text-gray-200">Risk Assessment Agent</h3>
              <span className="text-[9px] font-mono font-bold text-emerald-400">CONFIDENCE: {activeIncident.riskAssessment.confidence}</span>
            </div>

            {/* Score circle */}
            <div className="flex items-center justify-center py-2">
              <div className="relative flex items-center justify-center w-28 h-28 rounded-full border-4 border-white/5">
                {/* Visual glow indicator */}
                <div className={`absolute inset-0.5 rounded-full filter blur-[15px] opacity-10 ${
                  activeIncident.severity === 'CRITICAL' ? 'bg-rose-500 shadow-glow-purple' : 'bg-amber-500'
                }`}></div>
                <div className="text-center">
                  <div className="text-3xl font-extrabold text-gray-100">{activeIncident.riskAssessment.score}</div>
                  <div className="text-[10px] text-gray-400 font-mono font-bold uppercase">Risk Index</div>
                </div>
              </div>
            </div>

            {/* Risk details */}
            <div className="grid grid-cols-2 gap-4 text-center border-t border-white/5 pt-4">
              <div>
                <span className="text-[10px] text-gray-500 font-mono">SEVERITY LEVEL</span>
                <div className={`text-sm font-bold mt-0.5 ${
                  activeIncident.severity === 'CRITICAL' ? 'text-rose-400' :
                  activeIncident.severity === 'HIGH' ? 'text-amber-400' : 'text-emerald-400'
                }`}>{activeIncident.severity}</div>
              </div>
              <div>
                <span className="text-[10px] text-gray-500 font-mono">STATUS STATE</span>
                <div className="text-sm font-bold mt-0.5 text-gray-200">{activeIncident.status}</div>
              </div>
            </div>

            {/* Risk Factors list */}
            <div className="space-y-2 pt-2">
              <span className="text-[10px] text-gray-400 font-bold uppercase tracking-wider font-mono">Identified Risk Factors</span>
              <div className="space-y-1.5">
                {activeIncident.riskAssessment.riskFactors.map((fact, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-xs text-gray-300 font-mono bg-white/5 px-2.5 py-1.5 rounded-lg border border-white/5">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-400 shrink-0"></span>
                    <span className="truncate">{fact}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Agent B: Timeline Analysis Agent */}
          <div className="p-5 rounded-2xl glass-panel border border-white/5 shadow-glass space-y-4">
            <div className="flex justify-between items-center pb-3 border-b border-white/5">
              <h3 className="text-sm font-bold text-gray-200 flex items-center gap-2">
                <Clock className="w-4.5 h-4.5 text-indigo-400" />
                <span>Timeline Analysis Agent</span>
              </h3>
              <span className="text-[9px] font-mono text-gray-400 uppercase font-semibold">T-DUR: {activeIncident.timelineAnalysis.duration}</span>
            </div>

            {/* Vertical Stepper Timeline */}
            <div className="relative pl-4 space-y-5 border-l border-white/10 ml-2 py-1">
              {activeIncident.timelineAnalysis.sequence.map((event, idx) => (
                <div key={idx} className="relative">
                  {/* Stepper Dot */}
                  <span className={`
                    absolute -left-[21px] top-1.5 w-2.5 h-2.5 rounded-full border border-bg-darker
                    ${event.type === 'critical' ? 'bg-rose-500 shadow-glow-purple animate-ping' : 
                      event.type === 'warning' ? 'bg-amber-500' : 'bg-indigo-400'}
                  `}></span>
                  <div className="space-y-0.5 text-left">
                    <span className="text-[10px] text-indigo-400 font-mono font-bold">{event.time}</span>
                    <p className="text-xs text-gray-200 leading-normal">{event.event}</p>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="text-[10px] text-gray-500 font-mono border-t border-white/5 pt-3">
              Trigger Source Type: <span className="font-semibold text-gray-300">{activeIncident.timelineAnalysis.triggerType}</span>
            </div>
          </div>

          {/* Agent E: AI Recommendations */}
          <div className="p-5 rounded-2xl glass-panel border border-white/5 shadow-glass space-y-4">
            <div className="flex items-center gap-2.5 pb-3 border-b border-white/5">
              <ListChecks className="w-4.5 h-4.5 text-emerald-400" />
              <h3 className="text-sm font-bold text-gray-200">Agent Action Recommendations</h3>
            </div>

            <div className="space-y-3">
              {activeIncident.aiRecommendations.map((rec, idx) => (
                <div key={idx} className="flex gap-2.5 items-start p-2.5 rounded-lg bg-emerald-500/5 border border-emerald-500/10 text-xs text-gray-300">
                  <span className="flex items-center justify-center w-5 h-5 rounded bg-emerald-500/20 text-emerald-400 font-mono text-[10px] font-bold shrink-0 mt-0.5">
                    {idx + 1}
                  </span>
                  <p className="leading-normal">{rec}</p>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};

export default Analysis;
