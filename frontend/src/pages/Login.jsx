import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Terminal, ShieldAlert, KeyRound, Mail, ArrowRight } from 'lucide-react';

const Login = () => {
  const { login } = useApp();
  const navigate = useNavigate();
  const [email, setEmail] = useState('operator@smartops.ai');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Short timeout to simulate authentication delays
    setTimeout(() => {
      const success = login(email, password);
      setLoading(false);
      if (success) {
        navigate('/dashboard');
      } else {
        setError('Invalid credentials. Please enter a valid email and password.');
      }
    }, 800);
  };

  return (
    <div className="relative flex items-center justify-center min-h-screen px-4 overflow-hidden bg-bg-darker">
      {/* Background elements */}
      <div className="absolute top-1/4 left-1/4 w-[35rem] h-[35rem] rounded-full bg-indigo-900/10 blur-[130px] pointer-events-none -z-10 animate-glow" />
      <div className="absolute bottom-1/4 right-1/4 w-[35rem] h-[35rem] rounded-full bg-violet-900/10 blur-[130px] pointer-events-none -z-10 animate-pulse-slow" />
      
      {/* Login Card Container */}
      <div className="w-full max-w-md p-8 rounded-2xl glass-panel shadow-glass border border-white/10 z-10">
        
        {/* Brand/Header */}
        <div className="flex flex-col items-center mb-8 text-center">
          <div className="flex items-center justify-center w-14 h-14 mb-4 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-400 shadow-glow-indigo animate-float">
            <Terminal className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-200 via-indigo-100 to-violet-200">
            SmartOps AI
          </h1>
          <p className="mt-2 text-sm text-gray-400">
            Agentic Incident Intelligence Platform
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="flex items-start gap-2.5 p-3.5 mb-6 rounded-lg bg-rose-500/10 border border-rose-500/25 text-rose-400 text-xs">
            <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Email field */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-gray-300 uppercase tracking-wider">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3.5 top-3.5 w-4 h-4 text-gray-400" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="operator@smartops.ai"
                className="w-full py-3.5 pl-10 pr-4 text-sm glass-input"
              />
            </div>
          </div>

          {/* Password field */}
          <div className="space-y-1.5">
            <div className="flex justify-between items-center">
              <label className="text-xs font-semibold text-gray-300 uppercase tracking-wider">Password</label>
              <a href="#forgot" className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors">Forgot?</a>
            </div>
            <div className="relative">
              <KeyRound className="absolute left-3.5 top-3.5 w-4 h-4 text-gray-400" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full py-3.5 pl-10 pr-4 text-sm glass-input"
              />
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="flex items-center justify-center w-full gap-2 py-3.5 font-semibold text-sm rounded-xl text-white bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 transition-all duration-200 shadow-glow-indigo border border-indigo-400/20 disabled:opacity-50 cursor-pointer group"
          >
            {loading ? (
              <span className="w-5 h-5 rounded-full border-2 border-white/20 border-t-white animate-spin"></span>
            ) : (
              <>
                <span>Sign In to Terminal</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </form>

        {/* Demo Hint */}
        <div className="mt-8 text-center border-t border-white/5 pt-6">
          <p className="text-[11px] text-gray-500 font-mono">
            Demo credentials configured. Click Sign In to proceed.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
