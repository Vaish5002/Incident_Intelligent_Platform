import React, { useState } from 'react';
import { ShieldAlert, GitBranch, Cpu, Code, ExternalLink, GitCommit, User, Calendar, FileCode, ChevronDown, ChevronUp } from 'lucide-react';

const ResultCard = ({ incident }) => {
  if (!incident) return null;
  const [expandedChange, setExpandedChange] = useState(null);
  const [showFullDiff, setShowFullDiff] = useState(false);

  const renderDiffLine = (line, index) => {
    if (line.startsWith('+') && !line.startsWith('+++')) {
      return (
        <div key={index} className="text-emerald-400 bg-emerald-500/10 px-2 py-0.5 font-mono text-xs border-l-2 border-emerald-500">
          {line}
        </div>
      );
    } else if (line.startsWith('-') && !line.startsWith('---')) {
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

  const severityColor = {
    CRITICAL: 'text-rose-400 bg-rose-500/15 border-rose-500/25',
    HIGH: 'text-amber-400 bg-amber-500/15 border-amber-500/25',
    MEDIUM: 'text-yellow-400 bg-yellow-500/15 border-yellow-500/25',
    LOW: 'text-emerald-400 bg-emerald-500/15 border-emerald-500/25',
  };

  const { gitAnalysis } = incident;
  const repoUrl = gitAnalysis?.repoUrl || '';
  const commitUrl = gitAnalysis?.commitUrl || (
    repoUrl && gitAnalysis?.commitHash && gitAnalysis?.commitHash !== 'N/A'
      ? `${repoUrl.replace(/\/$/, '')}/commit/${gitAnalysis.commitHash}`
      : ''
  );

  return (
    <div className="space-y-6">

      {/* ── Risk / Severity / Impact stats ── */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-white/5 border border-white/5 text-center flex flex-col justify-center">
          <span className="text-[10px] text-gray-400 font-mono uppercase font-bold">Risk Index</span>
          <span className="text-3xl font-extrabold text-indigo-400 mt-1">{incident.riskAssessment.score} / 100</span>
          <span className="text-[9px] text-gray-500 mt-0.5 font-mono font-bold">CONFIDENCE: {incident.riskAssessment.confidence}</span>
        </div>

        <div className="p-4 rounded-xl bg-white/5 border border-white/5 text-center flex flex-col justify-center">
          <span className="text-[10px] text-gray-400 font-mono uppercase font-bold">Severity Level</span>
          <div className="mt-1">
            <span className={`inline-block px-3 py-1 rounded-md text-xs font-bold border ${
              severityColor[incident.severity] || 'text-gray-400 bg-white/5 border-white/10'
            } ${incident.severity === 'CRITICAL' ? 'animate-pulse' : ''}`}>
              {incident.severity}
            </span>
          </div>
          <span className="text-[9px] text-gray-500 mt-1 font-mono uppercase">Trigger: {incident.timelineAnalysis.triggerType}</span>
        </div>

        <div className="p-4 rounded-xl bg-white/5 border border-white/5 text-center flex flex-col justify-center">
          <span className="text-[10px] text-gray-400 font-mono uppercase font-bold">Impact Scope</span>
          <span className="text-xl font-bold text-gray-200 mt-1">{incident.activeUsersAffected} SRE Users</span>
          <span className="text-[9px] text-gray-500 mt-0.5 font-mono">DUR: {incident.timelineAnalysis.duration}</span>
        </div>
      </div>

      {/* ── Root Cause ── */}
      <div className="p-5 rounded-xl bg-indigo-600/5 border border-indigo-500/20 space-y-2 text-left">
        <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
          <Cpu className="w-4 h-4" />
          <span>Root Cause Diagnostics</span>
        </h4>
        <p className="text-sm text-gray-200 leading-relaxed font-semibold">
          {incident.logAnalysis.rootCause}
        </p>
      </div>

      {/* ── GitHub Commit Evidence Banner ── */}
      {gitAnalysis?.commitHash && gitAnalysis.commitHash !== 'N/A' && (
        <div className="p-4 rounded-xl bg-violet-600/5 border border-violet-500/20 flex flex-wrap items-center gap-4 text-xs font-mono">
          <div className="flex items-center gap-2 text-violet-400 font-bold">
            <GitCommit className="w-4 h-4" />
            <span>Causative Commit</span>
          </div>
          <div className="flex flex-wrap gap-3 text-gray-300 text-[11px]">
            <span className="flex items-center gap-1">
              <span className="text-gray-500">HASH:</span>
              <code className="bg-white/5 px-1.5 py-0.5 rounded text-violet-300">{gitAnalysis.commitHash}</code>
              {commitUrl && (
                <a href={commitUrl} target="_blank" rel="noopener noreferrer"
                   className="text-violet-400 hover:text-violet-200 transition-colors ml-1" title="View commit on GitHub">
                  <ExternalLink className="w-3 h-3 inline" />
                </a>
              )}
            </span>
            {gitAnalysis.author && gitAnalysis.author !== 'N/A' && (
              <span className="flex items-center gap-1">
                <User className="w-3 h-3 text-gray-500" />
                <span>{gitAnalysis.author}</span>
              </span>
            )}
            {repoUrl && (
              <a href={repoUrl} target="_blank" rel="noopener noreferrer"
                 className="flex items-center gap-1 text-indigo-400 hover:text-indigo-300 transition-colors">
                <ExternalLink className="w-3 h-3" />
                <span>Open Repository</span>
              </a>
            )}
          </div>
        </div>
      )}

      {/* ── Git Changes & Code Snippets ── */}
      <div className="p-5 rounded-xl bg-white/5 border border-white/5 space-y-4 text-left">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-white/10 pb-3">
          <h4 className="text-xs font-bold text-violet-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
            <GitBranch className="w-4 h-4" />
            <span>Code Changes Causing Failure</span>
          </h4>
          {gitAnalysis?.commitHash && gitAnalysis.commitHash !== 'N/A' && (
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-gray-500 font-mono">
                Commit: <span className="font-bold text-gray-300">{gitAnalysis.commitHash}</span>
              </span>
              {commitUrl && (
                <a href={commitUrl} target="_blank" rel="noopener noreferrer"
                   className="flex items-center gap-1 text-[10px] text-violet-400 hover:text-violet-300 font-mono transition-colors">
                  <ExternalLink className="w-3 h-3" />
                  <span>GitHub</span>
                </a>
              )}
            </div>
          )}
        </div>

        {incident.gitAnalysis.riskyCodeChanges.length > 0 ? (
          <div className="space-y-5">
            {incident.gitAnalysis.riskyCodeChanges.map((change, idx) => {
              const isExpanded = expandedChange === idx;
              const changeCommitUrl = change.commit_url || (
                repoUrl && change.commit
                  ? `${repoUrl.replace(/\/$/, '')}/commit/${change.commit}`
                  : commitUrl
              );
              const changeFileUrl = change.file_url || (
                repoUrl && change.commit && change.file
                  ? `${repoUrl.replace(/\/$/, '')}/blob/${change.commit}/${change.file}`
                  : ''
              );

              return (
                <div key={idx} className="rounded-xl border border-white/8 bg-black/20 overflow-hidden">
                  {/* Change header */}
                  <div className="px-4 py-3 flex flex-wrap justify-between items-start gap-2">
                    <div className="space-y-1 flex-1 min-w-0">
                      {/* File path with GitHub link */}
                      <div className="flex items-center gap-2 flex-wrap">
                        <FileCode className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                        <span className="text-[11px] font-mono text-indigo-300 font-bold">{change.file}</span>
                        {change.line && change.line !== 'N/A' && (
                          <span className="text-[9px] text-gray-500 font-mono">Line {change.line}</span>
                        )}
                        {changeFileUrl && (
                          <a href={changeFileUrl} target="_blank" rel="noopener noreferrer"
                             className="flex items-center gap-0.5 text-[9px] text-violet-400 hover:text-violet-300 font-mono transition-colors"
                             title="View file on GitHub">
                            <ExternalLink className="w-2.5 h-2.5" />
                            <span>View on GitHub</span>
                          </a>
                        )}
                      </div>
                      {/* Commit + author */}
                      <div className="flex items-center gap-3 text-[10px] text-gray-500 font-mono">
                        {change.commit && (
                          <span className="flex items-center gap-1">
                            <GitCommit className="w-2.5 h-2.5" />
                            <code>{change.commit}</code>
                            {changeCommitUrl && (
                              <a href={changeCommitUrl} target="_blank" rel="noopener noreferrer"
                                 className="text-violet-400 hover:text-violet-300 ml-0.5">
                                <ExternalLink className="w-2.5 h-2.5 inline" />
                              </a>
                            )}
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-0.5 rounded text-[9px] font-bold border uppercase ${
                        change.severity === 'CRITICAL' ? 'bg-rose-500/15 text-rose-400 border-rose-500/30' :
                        change.severity === 'HIGH' ? 'bg-amber-500/15 text-amber-400 border-amber-500/30' :
                        'bg-yellow-500/15 text-yellow-400 border-yellow-500/30'
                      }`}>
                        {change.severity} RISK
                      </span>
                      {change.codeSnippet && (
                        <button onClick={() => setExpandedChange(isExpanded ? null : idx)}
                                className="flex items-center gap-1 text-[10px] text-indigo-400 hover:text-indigo-300 font-mono transition-colors">
                          {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                          <span>{isExpanded ? 'Hide Code' : 'Show Code'}</span>
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Change description */}
                  <div className="px-4 pb-3">
                    <p className="text-xs text-gray-300 leading-normal bg-white/5 p-3 rounded-lg border border-white/5">
                      {change.change}
                    </p>
                  </div>

                  {/* Code Snippet (expandable) */}
                  {change.codeSnippet && isExpanded && (
                    <div className="px-4 pb-4 space-y-3">
                      <div className="flex items-center gap-2 text-[10px] text-gray-500 font-mono uppercase font-bold">
                        <Code className="w-3 h-3" />
                        <span>Problematic Code from Commit {change.commit}</span>
                        {changeCommitUrl && (
                          <a href={changeCommitUrl} target="_blank" rel="noopener noreferrer"
                             className="flex items-center gap-0.5 text-violet-400 hover:text-violet-300 ml-1">
                            <ExternalLink className="w-2.5 h-2.5" />
                            <span>GitHub</span>
                          </a>
                        )}
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {/* BEFORE */}
                        <div className="space-y-1">
                          <div className="text-[10px] text-rose-400 font-mono font-bold flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full bg-rose-500 inline-block"></span>
                            BEFORE — Original Working Code
                          </div>
                          <div className="bg-rose-500/5 border border-rose-500/20 rounded-lg p-3 overflow-x-auto">
                            <pre className="text-[11px] font-mono text-gray-300 whitespace-pre-wrap leading-relaxed">
                              {change.codeSnippet.before}
                            </pre>
                          </div>
                        </div>

                        {/* AFTER */}
                        <div className="space-y-1">
                          <div className="text-[10px] text-emerald-400 font-mono font-bold flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full bg-amber-500 inline-block"></span>
                            AFTER — Problematic Code Introduced
                          </div>
                          <div className="bg-amber-500/5 border border-amber-500/20 rounded-lg p-3 overflow-x-auto">
                            <pre className="text-[11px] font-mono text-gray-300 whitespace-pre-wrap leading-relaxed">
                              {change.codeSnippet.after}
                            </pre>
                          </div>
                        </div>
                      </div>

                      {/* Explanation */}
                      {change.explanation && (
                        <div className="p-3 rounded-lg bg-amber-500/5 border border-amber-500/20 text-xs text-amber-300 flex items-start gap-2">
                          <ShieldAlert className="w-3.5 h-3.5 mt-0.5 flex-shrink-0" />
                          <div>
                            <span className="font-bold text-amber-400 uppercase text-[10px] block mb-0.5">Why This Caused the Failure</span>
                            <span className="leading-relaxed">{change.explanation}</span>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}

            {/* ── Git Diff viewer ── */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-[10px] text-gray-500 font-mono uppercase font-bold">Complete Git Diff</span>
                <button onClick={() => setShowFullDiff(v => !v)}
                        className="text-[10px] text-indigo-400 hover:text-indigo-300 font-mono transition-colors flex items-center gap-1">
                  {showFullDiff ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                  {showFullDiff ? 'Collapse' : 'Expand'}
                </button>
              </div>
              <div className={`bg-black/30 border border-white/5 rounded-lg p-3.5 overflow-x-auto ${showFullDiff ? '' : 'max-h-48'} scrollbar flex flex-col gap-0.5 font-mono transition-all`}>
                {incident.gitAnalysis.diff.split('\n').map((line, idx) => renderDiffLine(line, idx))}
              </div>
              {!showFullDiff && (
                <p className="text-[9px] text-gray-600 font-mono text-center">
                  Showing partial diff — click Expand for full view
                </p>
              )}
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-6 text-center text-gray-500 space-y-2">
            <Code className="w-8 h-8 text-gray-600" />
            <p className="text-xs font-mono">No repository modifications identified.</p>
            <p className="text-[10px] text-gray-600">This incident is attributed to external API or service outages.</p>
          </div>
        )}
      </div>

    </div>
  );
};

export default ResultCard;
