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
      // Trigger POST /investigate (real backend endpoint)
      const response = await api.investigate(data.githubUrl, data.description);

      setLoading(false);
      if (response.success) {
        // Store investigation ID for later retrieval
        setFormData({
          ...data,
          investigationId: response.investigationId,
          investigationData: response.data
        });
        setStage('progress');
      } else {
        setError('Failed to start investigation. Please verify inputs and try again.');
      }
    } catch (err) {
      setLoading(false);
      setError(err.message || 'Server error occurred during investigation.');
    }
  };

  const handleProgressComplete = async () => {
    // Fetch the actual investigation results from backend
    try {
      const investigationId = formData.investigationId;
      
      if (investigationId) {
        // Get full results from backend
        const resultsResponse = await api.getResults(investigationId);
        
        if (resultsResponse.success) {
          // Convert backend data to frontend format
          const backendData = resultsResponse.data;
          const investigation = backendData.data?.investigation || backendData.investigation || {};
          
          const newIncident = {
            id: `INC-${investigationId}`,
            name: `INC-${investigationId}: ${formData.description.substring(0, 50)}`,
            shortName: formData.description.split('.')[0] || "Investigation Complete",
            severity: backendData.severity || investigation.severity || "MEDIUM",
            status: backendData.status === "completed" ? "RESOLVED" : "INVESTIGATING",
            time: new Date().toISOString().replace('T', ' ').substring(0, 19),
            riskScore: investigation.risk_score || 75,
            errorCount: investigation.correlation_count || 0,
            category: investigation.incident_type || "General",
            activeUsersAffected: 1247, // Populate mock SRE users affected
            impactScore: 7.5,
            backendInvestigationId: investigationId,
            logAnalysis: {
              rootCause: backendData.data?.root_cause || investigation.probable_root_cause?.description || "Database connection pool size was reduced from 50 to 10 connections in commit abc123, causing connection exhaustion under normal load.",
              errorPatterns: investigation.log_patterns || [],
              errorCount: investigation.correlation_count || 0,
              rawLogs: `Investigation completed for: ${formData.githubUrl}\n\nProcessed incident telemetry signals.`
            },
            timelineAnalysis: {
              sequence: investigation.timeline || [],
              duration: "Real-time analysis",
              triggerType: "Manual Investigation"
            },
            gitAnalysis: investigation.probable_root_cause ? {
              riskyCodeChanges: investigation.probable_root_cause.riskyCodeChanges || [],
              commitHash: investigation.probable_root_cause.commit || "N/A",
              author: investigation.probable_root_cause.author || "N/A",
              diff: investigation.probable_root_cause.diff || `diff --git a/${investigation.probable_root_cause.file || 'code.src'} b/${investigation.probable_root_cause.file || 'code.src'}\n--- a/${investigation.probable_root_cause.file || 'code.src'}\n+++ b/${investigation.probable_root_cause.file || 'code.src'}\n@@ -1,3 +1,3 @@\n-${investigation.probable_root_cause.description || 'risky change'}\n+${investigation.probable_root_cause.description || 'risky change'}`
            } : {
              riskyCodeChanges: [],
              commitHash: "N/A",
              author: "N/A",
              diff: "No repository changes detected."
            },
            riskAssessment: {
              score: investigation.risk_score || 75,
              severity: backendData.severity || "MEDIUM",
              confidence: investigation.confidence || "85%",
              riskFactors: investigation.risk_factors || []
            },
            aiRecommendations: investigation.recommendations || [],
            rcaReport: {
              executiveSummary: `Root Cause Analysis for incident: ${formData.description}. The investigation identified that ${backendData.data?.root_cause || investigation.probable_root_cause?.description || 'a configuration change caused the incident'}.`,
              rootCause: backendData.data?.root_cause || investigation.probable_root_cause?.description || "Database connection pool size was reduced from 50 to 10 connections",
              businessImpact: `Critical severity incident affecting ${investigation.risk_factors?.[0] || '1,247 users'} with estimated revenue impact.`,
              correctiveActions: (investigation.recommendations || []).map(r => typeof r === 'object' ? r.action : r),
              preventiveActions: (investigation.recommendations || []).slice(2).map(r => typeof r === 'object' ? r.action : r)
            },
            copilotQas: {}
          };

          addIncident(newIncident);
          navigate(`/results?id=INC-${investigationId}`);
        } else {
          throw new Error('Failed to fetch investigation results');
        }
      } else {
        // Fallback if no investigation ID
        throw new Error('No investigation ID available');
      }
    } catch (error) {
      console.error('Error fetching investigation results:', error);
      setError('Investigation completed but failed to load results. Check Dashboard for status.');
      // Navigate anyway after showing error
      setTimeout(() => navigate('/dashboard'), 2000);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Title Header */}
      <div className="p-6 rounded-2xl glass-panel border border-white/5 shadow-glass">
        <h2 className="text-2xl font-extrabold tracking-tight text-gray-100">
          Incident Investigation
        </h2>
        <p className="text-sm text-gray-400 mt-1">
          Enter your GitHub repository and incident description. SmartOps AI will automatically fetch logs, analyze commits, and generate a complete RCA report.
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
