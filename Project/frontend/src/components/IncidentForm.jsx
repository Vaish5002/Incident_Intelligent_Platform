import React, { useState } from 'react';
import { GitBranch, Play, AlertCircle } from 'lucide-react';

const IncidentForm = ({ onSubmit }) => {
  const [githubUrl, setGithubUrl] = useState('');
  const [description, setDescription] = useState('');
  
  // Validation errors state
  const [errors, setErrors] = useState({});

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

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit({
        githubUrl,
        description
      });
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
          placeholder="Describe symptoms, e.g., Users unable to complete payments after deployment"
          className={`w-full p-3.5 text-sm glass-input resize-none ${errors.description ? 'border-rose-500/50 focus:border-rose-500' : ''}`}
        />
        {errors.description && (
          <div className="text-xs text-rose-400 font-semibold flex items-center gap-1">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>{errors.description}</span>
          </div>
        )}
      </div>

      {/* Automatic Log Fetching Info */}
      <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            <svg className="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="flex-1 text-left">
            <p className="text-xs font-bold text-indigo-300 mb-1">Automatic Log Fetching</p>
            <p className="text-xs text-gray-400 leading-relaxed">
              SmartOps AI will automatically fetch runtime logs from the Chaos Demo Platform at <span className="font-mono text-indigo-400">https://chaos-demo-platform.onrender.com/logs</span>. No manual log upload required!
            </p>
          </div>
        </div>
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

export default IncidentForm;
