import React from 'react';
import { ShieldAlert, GitBranch, Cpu, Code } from 'lucide-react';

const ResultCard = ({ incident }) => {
  if (!incident) return null;

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
      
      {/* Risk and Severity Stats Header */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Risk Score */}
        <div className="p-4 rounded-xl bg-white/5 border border-white/5 text-center flex flex-col justify-center">
          <span className="text-[10px] text-gray-400 font-mono uppercase font-bold">Risk Index</span>
          <span className="text-3xl font-extrabold text-indigo-400 mt-1">{incident.riskAssessment.score} / 100</span>
          <span className="text-[9px] text-gray-500 mt-0.5 font-mono font-bold">CONFIDENCE: {incident.riskAssessment.confidence}</span>
        </div>

        {/* Severity */}
        <div className="p-4 rounded-xl bg-white/5 border border-white/5 text-center flex flex-col justify-center">
          <span className="text-[10px] text-gray-400 font-mono uppercase font-bold">Severity Level</span>
          <div className="mt-1">
            <span className={`inline-block px-3 py-1 rounded-md text-xs font-bold ${
              incident.severity === 'CRITICAL' ? 'bg-rose-500/15 text-rose-400 border border-rose-500/25 animate-pulse-slow' :
              incident.severity === 'HIGH' ? 'bg-amber-500/15 text-amber-400 border border-amber-500/25' :
              'bg-emerald-500/15 text-emerald-400 border border-emerald-500/25'
            }`}>
              {incident.severity}
            </span>
          </div>
          <span className="text-[9px] text-gray-500 mt-1 font-mono uppercase">Trigger: {incident.timelineAnalysis.triggerType}</span>
        </div>

        {/* Impact Scope */}
        <div className="p-4 rounded-xl bg-white/5 border border-white/5 text-center flex flex-col justify-center">
          <span className="text-[10px] text-gray-400 font-mono uppercase font-bold">Impact Scope</span>
          <span className="text-xl font-bold text-gray-200 mt-1">{incident.activeUsersAffected} SRE Users</span>
          <span className="text-[9px] text-gray-500 mt-0.5 font-mono">DUR: {incident.timelineAnalysis.duration}</span>
        </div>
      </div>

      {/* Root Cause card */}
      <div className="p-5 rounded-xl bg-indigo-600/5 border border-indigo-500/20 space-y-2 text-left">
        <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
          <Cpu className="w-4.5 h-4.5" />
          <span>Root Cause Diagnostics</span>
        </h4>
        <p className="text-sm text-gray-200 leading-relaxed font-semibold">
          {incident.logAnalysis.rootCause}
        </p>
      </div>

      {/* Git Changes & Commit Payload */}
      <div className="p-5 rounded-xl bg-white/5 border border-white/5 space-y-4 text-left">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-white/10 pb-3">
          <h4 className="text-xs font-bold text-violet-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
            <GitBranch className="w-4.5 h-4.5" />
            <span>Target Commit Modifications</span>
          </h4>
          {incident.gitAnalysis.commitHash !== 'N/A' && (
            <span className="text-[10px] text-gray-500 font-mono">
              Commit: <span className="font-bold text-gray-300">{incident.gitAnalysis.commitHash}</span>
            </span>
          )}
        </div>

        {incident.gitAnalysis.riskyCodeChanges.length > 0 ? (
          <div className="space-y-4">
            {incident.gitAnalysis.riskyCodeChanges.map((change, idx) => (
              <div key={idx} className="space-y-2">
                <div className="flex justify-between items-center text-xs font-mono">
                  <span className="text-indigo-400 font-bold">File: {change.file} (Line {change.line})</span>
                  <span className="px-2 py-0.5 rounded text-[9px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20 uppercase">
                    {change.severity} RISK
                  </span>
                </div>
                <p className="text-xs text-gray-300 leading-normal bg-white/5 p-3 rounded-lg border border-white/5">
                  {change.change}
                </p>
              </div>
            ))}

            {/* Diff Viewer */}
            <div className="space-y-1.5">
              <span className="text-[10px] text-gray-500 font-mono uppercase font-bold">Source Git Diff</span>
              <div className="bg-bg-darker border border-white/5 rounded-lg p-3.5 overflow-x-auto max-h-56 scrollbar flex flex-col gap-0.5 font-mono">
                {incident.gitAnalysis.diff.split('\n').map((line, idx) => renderDiffLine(line, idx))}
              </div>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-6 text-center text-gray-500 space-y-2">
            <Code className="w-8 h-8 text-gray-500" />
            <p className="text-xs font-mono">No repository modifications identified.</p>
            <p className="text-[10px] text-gray-500">This incident is attributed to external api/service outages.</p>
          </div>
        )}
      </div>

    </div>
  );
};

export default ResultCard;
