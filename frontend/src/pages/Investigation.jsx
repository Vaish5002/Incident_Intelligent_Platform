import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { api } from '../services/api';
import IncidentForm from '../components/IncidentForm';
import ProgressTracker from '../components/ProgressTracker';
import { Cpu } from 'lucide-react';

const Investigation = () => {
  const { addIncident } = useApp();
  const navigate = useNavigate();
  
  // States: 'input', 'progress'
  const [stage, setStage] = useState('input');
  const [formData, setFormData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFormSubmit = async (data) => {
    setError('');
    setLoading(true);
    setFormData(data);

    try {
      // Trigger POST /upload-log mock endpoint
      await api.uploadLog(data.logFile);
      
      // Trigger POST /investigate mock endpoint
      const response = await api.investigate(data.githubUrl, data.description);

      setLoading(false);
      if (response.success) {
        setStage('progress');
      } else {
        setError('Failed to register SRE investigation task. Please verify credentials.');
      }
    } catch (err) {
      setLoading(false);
      setError(err.message || 'Server error occurred during log ingestion.');
    }
  };

  const handleProgressComplete = () => {
    // Generate a new custom incident based on inputs and redirect
    const randomIdNum = Math.floor(Math.random() * 1000) + 3100;
    const newIncId = `INC-${randomIdNum}`;

    const newIncident = {
      id: newIncId,
      name: `${newIncId}: Custom Hackathon Ingestion`,
      shortName: formData.description.split('.')[0] || "Custom Ingestion",
      severity: "HIGH",
      status: "INVESTIGATING",
      time: new Date().toISOString().replace('T', ' ').substring(0, 19),
      riskScore: 88,
      errorCount: 194,
      category: "GitHub Source",
      activeUsersAffected: 180,
      impactScore: 8.2,
      logAnalysis: {
        rootCause: `GitHub Ingestion analysis finalized. Repository [${formData.githubUrl}] contains warning logs in uploaded file: ${formData.logFile.name}. \nContext description details: ${formData.description}.`,
        errorPatterns: [
          "ERR: Connection timed out in git adapter threads",
          "WARN: Hikari pool queue threshold limits reached"
        ],
        errorCount: 194,
        rawLogs: `Ingested log metadata from [${formData.logFile.name}]:\n` +
                 `2026-06-08 12:05:00.112 - Fetching repo metadata from ${formData.githubUrl}\n` +
                 `2026-06-08 12:05:02.402 - Log Agent parsed stack trace successfully\n` +
                 `2026-06-08 12:05:04.912 - WARN: Connection timed out`
      },
      timelineAnalysis: {
        sequence: [
          { time: "12:05:00", event: "GitHub URL verified and repo index cataloged.", type: "info" },
          { time: "12:05:02", event: "Log analysis agent identified diagnostic trace signatures.", type: "warning" },
          { time: "12:05:04", event: "AI Agents correlated commit diff and confirmed index regression.", type: "critical" }
        ],
        duration: "12 minutes",
        triggerType: "GitHub Webhook / Manual Ingest"
      },
      gitAnalysis: {
        riskyCodeChanges: [
          {
            file: "src/connector/GatewayAdapter.js",
            line: 52,
            change: "Modified connection timeout limits on Git main branch.",
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
+  const socket = new NetSocket({ timeout: 60000 }); // Timeout limit extended`
      },
      riskAssessment: {
        score: 88,
        severity: "HIGH",
        confidence: "85%",
        riskFactors: [
          "GitHub Adapter timeout variables altered",
          "High volume warnings parsed in log ingest",
          "Database connection queues saturated"
        ]
      },
      aiRecommendations: [
        "Review GatewayAdapter.js connection parameters.",
        "Ensure query locks do not hold active connection pools.",
        "Set alert filters to capture thread count slopes early."
      ],
      rcaReport: {
        executiveSummary: `RCA for ${formData.description}. Repository URL: ${formData.githubUrl}. Ingested diagnostics from ${formData.logFile.name}.`,
        rootCause: "A connection timeout variable extension on the main branch caused threads to hang, saturating connection channels.",
        businessImpact: "Slowed down active user checkouts and checkout sync tasks.",
        correctiveActions: [
          "Reset connection configs to 5000ms.",
          "Restart network routing replicas."
        ],
        preventiveActions: [
          "Add static unit tests for time parameters.",
          "Verify thread slope indicators."
        ]
      },
      copilotQas: {
        "Why did this incident happen?": "The incident happened because socket connection timeout settings were raised to 60s, holding threads open.",
        "What failed first?": "Network adapter sockets timed out and blocked connection ports.",
        "How can this be prevented?": "Configure automated pool limits and reject PRs raising timeouts past 5000ms.",
        "Which code change caused the issue?": "The diff indicates a change in `GatewayAdapter.js` at line 52."
      }
    };

    addIncident(newIncident);
    navigate('/results');
  };

  return (
    <div className="space-y-6">
      
      {/* Title Header */}
      <div className="p-6 rounded-2xl glass-panel border border-white/5 shadow-glass">
        <h2 className="text-2xl font-extrabold tracking-tight text-gray-100">
          Incident Ingestion Pipeline
        </h2>
        <p className="text-sm text-gray-400 mt-1">
          Hook in your repository repositories and upload log files. SmartOps agents will automatically locate the source error.
        </p>
      </div>

      {stage === 'input' ? (
        <div className="p-6 rounded-2xl glass-panel border border-white/5 shadow-glass relative">
          
          {loading && (
            <div className="absolute inset-0 bg-bg-darker/60 backdrop-blur-sm z-20 flex flex-col items-center justify-center space-y-3 rounded-2xl">
              <span className="w-8 h-8 rounded-full border-2 border-indigo-500/20 border-t-indigo-500 animate-spin"></span>
              <span className="text-xs font-mono text-indigo-400 font-bold">Uploading logs & starting agents...</span>
            </div>
          )}

          {error && (
            <div className="p-3.5 mb-6 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs text-left">
              {error}
            </div>
          )}

          <IncidentForm onSubmit={handleFormSubmit} />
        </div>
      ) : (
        <ProgressTracker onComplete={handleProgressComplete} />
      )}

    </div>
  );
};

export default Investigation;
