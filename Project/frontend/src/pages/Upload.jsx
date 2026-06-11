import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { 
  Upload, 
  FileText, 
  FileSpreadsheet, 
  Code2, 
  Play, 
  AlertTriangle, 
  CheckCircle2, 
  Loader2 
} from 'lucide-react';

const FileDropZone = ({ 
  label, 
  accepts, 
  icon: Icon, 
  file, 
  onFileSelect, 
  error, 
  placeholder 
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      validateAndSetFile(files[0]);
    }
  };

  const handleFileChange = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      validateAndSetFile(files[0]);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    const extension = '.' + selectedFile.name.split('.').pop().toLowerCase();
    const isAccepted = accepts.split(',').some(ext => {
      const cleanExt = ext.trim().toLowerCase();
      return extension === cleanExt;
    });

    if (isAccepted) {
      onFileSelect(selectedFile, null);
    } else {
      onFileSelect(null, `Invalid file type. Please upload a ${accepts} file.`);
    }
  };

  return (
    <div className="space-y-1.5 flex-1">
      <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider">{label}</label>
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`
          relative flex flex-col items-center justify-center p-5 rounded-xl border border-dashed text-center cursor-pointer transition-all duration-200 h-36
          ${isDragOver 
            ? 'border-indigo-400 bg-indigo-500/5 shadow-glow-indigo' 
            : file 
              ? 'border-emerald-500/30 bg-emerald-500/5' 
              : error 
                ? 'border-rose-500/30 bg-rose-500/5' 
                : 'border-white/10 bg-white/5 hover:bg-white/10 hover:border-white/20'}
        `}
      >
        <input
          type="file"
          ref={fileInputRef}
          accept={accepts}
          onChange={handleFileChange}
          className="hidden"
        />

        {file ? (
          <div className="flex flex-col items-center space-y-2 text-emerald-400">
            <CheckCircle2 className="w-8 h-8 animate-bounce" />
            <span className="text-xs font-bold font-mono truncate max-w-[180px]">{file.name}</span>
            <span className="text-[10px] text-gray-500 font-mono">
              {(file.size / 1024).toFixed(1)} KB
            </span>
          </div>
        ) : (
          <div className="flex flex-col items-center space-y-2 text-gray-400">
            <div className={`p-2 rounded-lg ${error ? 'bg-rose-500/10 text-rose-400' : 'bg-white/5 text-gray-400'}`}>
              <Icon className="w-6 h-6" />
            </div>
            <span className="text-xs font-bold text-gray-200">
              Drag & drop or <span className="text-indigo-400 underline">browse</span>
            </span>
            <span className="text-[10px] text-gray-500 font-mono">{placeholder}</span>
          </div>
        )}

        {error && (
          <div className="absolute bottom-2 left-2 right-2 text-[10px] text-rose-400 font-semibold truncate flex items-center justify-center gap-1 bg-bg-darker/90 py-0.5 rounded">
            <AlertTriangle className="w-3 h-3 shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </div>
    </div>
  );
};

const UploadPage = () => {
  const { addIncident } = useApp();
  const navigate = useNavigate();
  
  const [incidentName, setIncidentName] = useState('');
  const [logFile, setLogFile] = useState(null);
  const [logError, setLogError] = useState('');
  
  const [csvFile, setCsvFile] = useState(null);
  const [csvError, setCsvError] = useState('');

  const [diffFile, setDiffFile] = useState(null);
  const [diffError, setDiffError] = useState('');

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [agentStep, setAgentStep] = useState('');

  const handleLogSelect = (file, err) => {
    setLogFile(file);
    setLogError(err || '');
  };

  const handleCsvSelect = (file, err) => {
    setCsvFile(file);
    setCsvError(err || '');
  };

  const handleDiffSelect = (file, err) => {
    setDiffFile(file);
    setDiffError(err || '');
  };

  const handleAnalyze = (e) => {
    e.preventDefault();
    if (!incidentName.trim()) return;

    setIsAnalyzing(true);
    setProgress(0);

    const steps = [
      { text: "Spawning Log Analysis Agent...", p: 20 },
      { text: "Log Analysis: Identified PostgreSQL exception in connection block", p: 40 },
      { text: "Spawning Timeline Agent: Correlating database logs and traffic spikes...", p: 60 },
      { text: "Spawning Git Agent: Identifying code alterations and deployment triggers...", p: 80 },
      { text: "Risk Assessment Agent: Running risk model index computations...", p: 95 },
      { text: "Consolidating Agent Findings and generating recommendations...", p: 100 }
    ];

    let currentStep = 0;

    const interval = setInterval(() => {
      if (currentStep < steps.length) {
        setAgentStep(steps[currentStep].text);
        setProgress(steps[currentStep].p);
        currentStep++;
      } else {
        clearInterval(interval);
        
        // Add incident to global context
        const randomIdNum = Math.floor(Math.random() * 1000) + 3100;
        const newIncId = `INC-${randomIdNum}`;
        
        const newIncident = {
          id: newIncId,
          name: `${newIncId}: ${incidentName}`,
          shortName: incidentName,
          severity: "HIGH",
          status: "INVESTIGATING",
          time: new Date().toISOString().replace('T', ' ').substring(0, 19),
          riskScore: 84,
          errorCount: 142,
          category: "Uploaded Source",
          activeUsersAffected: 320,
          impactScore: 7.8,
          logAnalysis: {
            rootCause: `Manual Upload Ingestion. Parsed logs point to an infrastructure warning related to: ${logFile ? logFile.name : 'Unknown log source'}.`,
            errorPatterns: [
              "ERR: System socket timeout on connection handler",
              "WARNING: Retrying gateway transmission slots"
            ],
            errorCount: 142,
            rawLogs: `Uploaded log snippet from file [${logFile ? logFile.name : 'N/A'}]:\n` +
                     `2026-06-08 12:00:01.002 SYSTEM - Initializing log ingestion pipeline\n` +
                     `2026-06-08 12:00:04.918 WARN  - [com.smartops.connector] - Socket failure, retry attempt #1\n` +
                     `2026-06-08 12:00:09.112 ERROR - SocketException: Connection refused`
          },
          timelineAnalysis: {
            sequence: [
              { time: "12:00:01", event: "File upload initialized and logs ingested.", type: "info" },
              { time: "12:00:04", event: "API Gateway returns SocketException.", type: "warning" },
              { time: "12:00:09", event: "Log Analysis Agent flagged socket exhaustion.", type: "critical" }
            ],
            duration: "8 minutes",
            triggerType: "Manual Upload Ingestion"
          },
          gitAnalysis: {
            riskyCodeChanges: [
              {
                file: "src/connector/GatewayAdapter.js",
                line: 52,
                change: `Suspicious code modification identified in Git Diff: ${diffFile ? diffFile.name : 'N/A'}.`,
                severity: "HIGH"
              }
            ],
            commitHash: "git-custom-88",
            author: "operator@smartops.ai",
            diff: `diff --git a/src/connector/GatewayAdapter.js b/src/connector/GatewayAdapter.js
index c892182..a99281a 100644
--- a/src/connector/GatewayAdapter.js
+++ b/src/connector/GatewayAdapter.js
@@ -52,3 +52,3 @@
-  const socket = new NetSocket({ timeout: 5000 });
+  const socket = new NetSocket({ timeout: 60000 }); // Risky Timeout Extension`
          },
          riskAssessment: {
            score: 84,
            severity: "HIGH",
            confidence: "82%",
            riskFactors: [
              "Socket connection timeouts observed",
              "Timeout threshold raised to 60s",
              "CSV logs correlate with gateway gateway errors"
            ]
          },
          aiRecommendations: [
            "Review Socket Timeout parameters in GatewayAdapter.js.",
            "Compare API response records from CSV with production network latency logs.",
            "Verify network load balances are correctly distributing WebSocket instances."
          ],
          rcaReport: {
            executiveSummary: `Custom uploaded incident analysis for ${incidentName}. Source files uploaded: ${logFile?.name}, ${csvFile?.name}, ${diffFile?.name}.`,
            rootCause: "A connection adapter timeout parameter extension was detected, which held open thread states under load and generated socket exception failures.",
            businessImpact: "Medium service interruption. Users reported slower page loads during checkout sync actions.",
            correctiveActions: [
              "Hot-reboot of socket gateway replicas.",
              "Reset connection config parameters to 5000ms."
            ],
            preventiveActions: [
              "Introduce automated unit tests for timeout constraints.",
              "Add telemetry alerting for socket count slopes."
            ]
          },
          copilotQas: {
            "Why did this incident happen?": "The incident occurred because the socket connection timeout was modified from 5s to 60s, causing thread hangs when connections stalled.",
            "What failed first?": "Network sockets bound to client gateways timed out and crashed.",
            "How can this be prevented?": "Revert the socket timeout parameter to a lower threshold and set up connection pool monitors.",
            "Which code change caused the issue?": "The diff shows a modification in `GatewayAdapter.js` at line 52."
          }
        };

        addIncident(newIncident);
        setIsAnalyzing(false);
        navigate('/analysis');
      }
    }, 900);
  };

  return (
    <div className="space-y-6">
      
      {/* Title block */}
      <div className="p-6 rounded-2xl glass-panel border border-white/5 shadow-glass">
        <h2 className="text-2xl font-extrabold tracking-tight text-gray-100">
          Incident Ingestion Pipeline
        </h2>
        <p className="text-sm text-gray-400 mt-1">
          Upload logs, events, and code diffs to trigger agentic reasoning models. SmartOps agents will automatically locate the root cause.
        </p>
      </div>

      {isAnalyzing ? (
        /* Ingest & Analysis Progress Animation */
        <div className="flex flex-col items-center justify-center p-16 rounded-2xl glass-panel border border-white/5 shadow-glass text-center space-y-6 min-h-[400px]">
          <div className="relative flex items-center justify-center">
            <Loader2 className="w-16 h-16 text-indigo-500 animate-spin" />
            <span className="absolute text-xs font-mono font-bold text-indigo-300">{progress}%</span>
          </div>
          <div className="space-y-2 max-w-md">
            <h4 className="text-lg font-bold text-gray-200">Analyzing Ingested Incident Data</h4>
            <div className="text-xs font-mono text-indigo-400 h-6 truncate animate-pulse">
              {agentStep}
            </div>
            
            {/* Custom progress bar */}
            <div className="w-64 h-1.5 bg-white/5 rounded-full overflow-hidden mx-auto mt-2">
              <div 
                className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 transition-all duration-300 rounded-full"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        </div>
      ) : (
        /* Form configuration */
        <form onSubmit={handleAnalyze} className="space-y-6">
          <div className="p-6 rounded-2xl glass-panel border border-white/5 shadow-glass space-y-6">
            
            {/* Input name */}
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-gray-300 uppercase tracking-wider">
                Incident Identifier Name
              </label>
              <input
                type="text"
                required
                value={incidentName}
                onChange={(e) => setIncidentName(e.target.value)}
                placeholder="e.g. Memory Spike in Billing Service, Gateway Timeout spikes"
                className="w-full p-3.5 text-sm glass-input"
              />
            </div>

            {/* Ingestion blocks (3 files) */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              {/* Logs Upload */}
              <FileDropZone
                label="System Logs File"
                accepts=".txt,.log"
                icon={FileText}
                file={logFile}
                onFileSelect={handleLogSelect}
                error={logError}
                placeholder="Supports .log, .txt"
              />

              {/* Timeline CSV Upload */}
              <FileDropZone
                label="Timeline CSV File"
                accepts=".csv"
                icon={FileSpreadsheet}
                file={csvFile}
                onFileSelect={handleCsvSelect}
                error={csvError}
                placeholder="Supports .csv"
              />

              {/* Git Diff Upload */}
              <FileDropZone
                label="Git Diff File"
                accepts=".txt"
                icon={Code2}
                file={diffFile}
                onFileSelect={handleDiffSelect}
                error={diffError}
                placeholder="Supports .txt (diff)"
              />

            </div>

            {/* Run Button Container */}
            <div className="border-t border-white/5 pt-6 flex justify-end">
              <button
                type="submit"
                disabled={!incidentName.trim() || !logFile}
                className="flex items-center gap-2 px-6 py-3.5 text-sm font-semibold rounded-xl text-white bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-200 shadow-glow-indigo cursor-pointer"
              >
                <Play className="w-4 h-4 fill-white" />
                <span>Ingest & Analyze Incident</span>
              </button>
            </div>

          </div>
        </form>
      )}

    </div>
  );
};

export default UploadPage;
