import React, { useState, useRef } from 'react';
import { Mail, GitBranch, FileText, Play, AlertCircle } from 'lucide-react';

const IncidentForm = ({ onSubmit }) => {
  const [githubUrl, setGithubUrl] = useState('');
  const [description, setDescription] = useState('');
  const [logFile, setLogFile] = useState(null);
  
  // Validation errors state
  const [errors, setErrors] = useState({});
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const validateForm = () => {
    const newErrors = {};
    
    // GitHub URL regex validation
    const githubRegex = /^https?:\/\/(www\.)?github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_.-]+(\/)?$/;
    if (!githubUrl) {
      newErrors.githubUrl = "GitHub Repository URL is required.";
    } else if (!githubRegex.test(githubUrl)) {
      newErrors.githubUrl = "Please enter a valid GitHub repository URL (e.g., https://github.com/owner/repo).";
    }

    // Description validation
    if (!description.trim()) {
      newErrors.description = "Incident description is required to provide context.";
    } else if (description.trim().length < 10) {
      newErrors.description = "Please provide a more descriptive summary (minimum 10 characters).";
    }

    // Log File validation
    if (!logFile) {
      newErrors.logFile = "Log file upload is required for root cause analysis.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit({
        githubUrl,
        description,
        logFile
      });
    }
  };

  // Drag and drop logic
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

  const validateAndSetFile = (file) => {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (ext === '.txt' || ext === '.log') {
      setLogFile(file);
      setErrors(prev => ({ ...prev, logFile: null }));
    } else {
      setLogFile(null);
      setErrors(prev => ({ ...prev, logFile: "Invalid file type. Please upload a .txt or .log file." }));
    }
  };

  return (
    <form onSubmit={handleFormSubmit} className="space-y-6">
      
      {/* GitHub Repository URL */}
      <div className="space-y-2 text-left">
        <label className="text-xs font-bold text-gray-300 uppercase tracking-wider flex items-center gap-1.5">
          <GitBranch className="w-4 h-4 text-indigo-400" />
          <span>GitHub Repository URL</span>
        </label>
        <input
          type="text"
          value={githubUrl}
          onChange={(e) => setGithubUrl(e.target.value)}
          placeholder="https://github.com/smartops-ai/core-billing-service"
          className={`w-full p-3.5 text-sm glass-input ${errors.githubUrl ? 'border-rose-500/50 focus:border-rose-500' : ''}`}
        />
        {errors.githubUrl && (
          <div className="text-xs text-rose-400 font-semibold flex items-center gap-1">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>{errors.githubUrl}</span>
          </div>
        )}
      </div>

      {/* Incident Description */}
      <div className="space-y-2 text-left">
        <label className="text-xs font-bold text-gray-300 uppercase tracking-wider">
          Incident Description / Symptoms
        </label>
        <textarea
          rows={3}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Describe symptoms, e.g., CPU utilization spiked after canary deployment, resulting in DB timeouts."
          className={`w-full p-3.5 text-sm glass-input resize-none ${errors.description ? 'border-rose-500/50 focus:border-rose-500' : ''}`}
        />
        {errors.description && (
          <div className="text-xs text-rose-400 font-semibold flex items-center gap-1">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>{errors.description}</span>
          </div>
        )}
      </div>

      {/* Log File Dropzone */}
      <div className="space-y-2 text-left">
        <label className="text-xs font-bold text-gray-300 uppercase tracking-wider flex items-center gap-1.5">
          <FileText className="w-4 h-4 text-indigo-400" />
          <span>System Diagnostics Log Ingest</span>
        </label>
        
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`
            relative flex flex-col items-center justify-center p-6 rounded-xl border border-dashed text-center cursor-pointer transition-all duration-200 h-36
            ${isDragOver 
              ? 'border-indigo-400 bg-indigo-500/5 shadow-glow-indigo' 
              : logFile 
                ? 'border-emerald-500/30 bg-emerald-500/5' 
                : errors.logFile 
                  ? 'border-rose-500/30 bg-rose-500/5' 
                  : 'border-white/10 bg-white/5 hover:bg-white/10 hover:border-white/20'}
          `}
        >
          <input
            type="file"
            ref={fileInputRef}
            accept=".txt,.log"
            onChange={handleFileChange}
            className="hidden"
          />

          {logFile ? (
            <div className="flex flex-col items-center space-y-1 text-emerald-400">
              <CheckCircleIcon className="w-8 h-8 text-emerald-400 shrink-0" />
              <span className="text-xs font-bold font-mono truncate max-w-[240px] mt-1">{logFile.name}</span>
              <span className="text-[10px] text-gray-500 font-mono">{(logFile.size / 1024).toFixed(1)} KB</span>
            </div>
          ) : (
            <div className="flex flex-col items-center space-y-1.5 text-gray-400">
              <FileText className="w-6 h-6 text-gray-400" />
              <span className="text-xs font-bold text-gray-200">
                Drag & drop log files or <span className="text-indigo-400 underline">browse</span>
              </span>
              <span className="text-[10px] text-gray-500 font-mono">Accepts .txt, .log</span>
            </div>
          )}
        </div>
        {errors.logFile && (
          <div className="text-xs text-rose-400 font-semibold flex items-center gap-1">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>{errors.logFile}</span>
          </div>
        )}
      </div>

      {/* Action Submit */}
      <div className="border-t border-white/5 pt-6 flex justify-end">
        <button
          type="submit"
          className="flex items-center gap-2 px-6 py-3.5 text-sm font-semibold rounded-xl text-white bg-indigo-600 hover:bg-indigo-500 transition-all duration-200 shadow-glow-indigo cursor-pointer"
        >
          <Play className="w-4 h-4 fill-white" />
          <span>Investigate</span>
        </button>
      </div>

    </form>
  );
};

// Simple helper icon
const CheckCircleIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

export default IncidentForm;
