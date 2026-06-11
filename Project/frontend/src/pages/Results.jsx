import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { api } from '../services/api';
import ResultCard from '../components/ResultCard';
import Recommendations from '../components/Recommendations';
import { Cpu, Download, FileText, ChevronDown, Check } from 'lucide-react';

const Results = () => {
  const { incidents, activeIncidentId, setActiveIncidentId, activeIncident } = useApp();
  const [downloading, setDownloading] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  if (!activeIncident) {
    return (
      <div className="p-8 text-center text-gray-400 font-mono">
        Loading SRE investigation results...
      </div>
    );
  }

  const handlePdfDownload = async () => {
    setDownloading(true);
    setDownloadSuccess(false);
    
    try {
      // Extract investigation ID from incident ID (format: INC-123 -> 123)
      const investigationId = activeIncidentId.replace('INC-', '');
      
      // Trigger GET /api/pdf/generate-from-incident/:id (Member 3)
      await api.downloadPdf(investigationId);
      
      setDownloading(false);
      setDownloadSuccess(true);
      
      // Clear success check after 3s
      setTimeout(() => setDownloadSuccess(false), 3000);
    } catch (err) {
      setDownloading(false);
      alert(err.message || 'Failed to download PDF report. Ensure Member 3 backend is running.');
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Title bar */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 p-5 rounded-2xl glass-panel border border-white/5 shadow-glass">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 font-bold text-xs uppercase tracking-wider">
            <Cpu className="w-4 h-4" />
            <span>Agentic Diagnostic Findings</span>
          </div>
          <h2 className="text-2xl font-extrabold text-gray-100 mt-1">
            Investigation Results
          </h2>
        </div>

        {/* Action controls */}
        <div className="flex flex-wrap items-center gap-3">
          <label className="text-xs text-gray-400 font-mono">Target Case:</label>
          <div className="relative">
            <select
              value={activeIncidentId}
              onChange={(e) => setActiveIncidentId(e.target.value)}
              className="pl-3 pr-8 py-2 text-xs font-mono font-bold rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-gray-200 outline-none cursor-pointer appearance-none min-w-[220px]"
            >
              {incidents.map((inc) => (
                <option key={inc.id} value={inc.id} className="bg-bg-darker text-gray-200">
                  {inc.id}: {inc.shortName}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-2.5 w-3.5 h-3.5 text-gray-400 pointer-events-none" />
          </div>

          <button
            onClick={handlePdfDownload}
            disabled={downloading}
            className="flex items-center gap-2 px-4 py-2.5 text-xs font-bold rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white shadow-glow-indigo transition-all cursor-pointer"
          >
            {downloading ? (
              <span className="w-3.5 h-3.5 rounded-full border border-white/20 border-t-white animate-spin"></span>
            ) : downloadSuccess ? (
              <Check className="w-3.5 h-3.5 text-emerald-300" />
            ) : (
              <Download className="w-3.5 h-3.5" />
            )}
            <span>Download RCA PDF</span>
          </button>
        </div>
      </div>

      {/* Main Results Card */}
      <div className="p-6 rounded-2xl glass-panel border border-white/5 shadow-glass space-y-6">
        {/* Header summary info */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-white/10">
          <div>
            <h3 className="text-lg font-bold text-gray-100">{activeIncident.shortName}</h3>
            <span className="text-[10px] text-gray-500 font-mono font-semibold">{activeIncident.name}</span>
          </div>
          <div className="text-right text-xs font-mono text-gray-400">
            Ingestion Date: <span className="font-semibold text-gray-300">{activeIncident.time}</span>
          </div>
        </div>

        {/* Modular ResultCard */}
        <ResultCard incident={activeIncident} />

        {/* Modular Recommendations timeline */}
        <Recommendations incident={activeIncident} />
      </div>

    </div>
  );
};

export default Results;
