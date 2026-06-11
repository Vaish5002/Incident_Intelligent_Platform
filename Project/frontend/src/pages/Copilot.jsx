import React, { useState, useEffect, useRef } from 'react';
import { useApp } from '../context/AppContext';
import { 
  MessageSquare, 
  Send, 
  Terminal, 
  Cpu, 
  Sparkles, 
  HelpCircle,
  Clock,
  ArrowDown
} from 'lucide-react';

const Copilot = () => {
  const { activeIncident } = useApp();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);

  const suggestedQuestions = [
    "Why did this incident happen?",
    "What failed first?",
    "How can this be prevented?",
    "Which code change caused the issue?"
  ];

  // Initialize chat when activeIncident changes
  useEffect(() => {
    if (activeIncident) {
      setMessages([
        {
          id: 'system',
          sender: 'copilot',
          text: `Hello SRE Operator! I have finished running my analytical reasoning models on **${activeIncident.id}** (${activeIncident.shortName}). I am ready to assist in your investigation. How can I help you troubleshoot?`,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    }
  }, [activeIncident]);

  // Scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSendMessage = (text) => {
    if (!text.trim()) return;

    const userMessage = {
      id: `msg-${Date.now()}-user`,
      sender: 'user',
      text: text,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // AI Response generation
    setTimeout(() => {
      let responseText = '';
      
      // Match question from suggested Q&As or generate generic SRE response
      const cleanText = text.trim();
      if (activeIncident.copilotQas && activeIncident.copilotQas[cleanText]) {
        responseText = activeIncident.copilotQas[cleanText];
      } else {
        responseText = `I have scanned the logs and code repositories for ${activeIncident.id}. While that specific question is outside my pre-compiled report indices, my heuristic models recommend checking:
1. Active DB thread states (currently hovering around critical levels).
2. Checkouts and upstream network gateway timings.
3. Commit diff history surrounding recent deployment windows.
Is there any specific log block you'd like me to parse?`;
      }

      const copilotMessage = {
        id: `msg-${Date.now()}-copilot`,
        sender: 'copilot',
        text: responseText,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => [...prev, copilotMessage]);
      setIsTyping(false);
    }, 1200);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage(inputValue);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Title block */}
      <div className="p-5 rounded-2xl glass-panel border border-white/5 shadow-glass flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 font-bold text-xs uppercase tracking-wider">
            <Sparkles className="w-4 h-4 animate-pulse-slow" />
            <span>SmartOps Copilot</span>
          </div>
          <h2 className="text-2xl font-extrabold text-gray-100 mt-1">
            AI Copilot Chat
          </h2>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/25 text-xs text-indigo-300 font-mono">
          <Cpu className="w-3.5 h-3.5" />
          <span>Active Context: {activeIncident?.id}</span>
        </div>
      </div>

      {/* Chat Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch h-[calc(100vh-16rem)]">
        
        {/* Chat Window - 8 Columns */}
        <div className="lg:col-span-8 flex flex-col p-5 rounded-2xl glass-panel border border-white/5 shadow-glass h-full overflow-hidden">
          
          {/* Messages Scroller */}
          <div className="flex-1 overflow-y-auto pr-2 space-y-4 mb-4 scrollbar">
            {messages.map((msg) => (
              <div 
                key={msg.id}
                className={`flex gap-3 max-w-[85%] ${msg.sender === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
              >
                {/* Avatar */}
                <div className={`
                  flex items-center justify-center w-8 h-8 rounded-lg shrink-0 border
                  ${msg.sender === 'user' 
                    ? 'bg-indigo-600/30 border-indigo-500/40 text-indigo-300' 
                    : 'bg-violet-600/30 border-violet-500/40 text-violet-300'}
                `}>
                  {msg.sender === 'user' ? <Terminal className="w-4.5 h-4.5" /> : <Cpu className="w-4.5 h-4.5" />}
                </div>

                {/* Bubble */}
                <div className="space-y-1">
                  <div className={`
                    p-3.5 rounded-2xl text-sm leading-relaxed
                    ${msg.sender === 'user' 
                      ? 'bg-indigo-600/20 border border-indigo-500/30 rounded-tr-none text-indigo-100' 
                      : 'bg-white/5 border border-white/5 rounded-tl-none text-gray-200'}
                  `}>
                    <p className="whitespace-pre-line">{msg.text}</p>
                  </div>
                  <div className="text-[10px] text-gray-500 font-mono text-right px-1">
                    {msg.time}
                  </div>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex gap-3 mr-auto max-w-[85%]">
                <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-violet-600/20 border border-violet-500/30 text-violet-400 shrink-0">
                  <Cpu className="w-4.5 h-4.5 animate-spin" />
                </div>
                <div className="bg-white/5 border border-white/5 p-3.5 rounded-2xl rounded-tl-none text-xs text-gray-400 font-mono flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce"></span>
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce [animation-delay:0.2s]"></span>
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce [animation-delay:0.4s]"></span>
                  <span className="ml-1 text-gray-500">Agent thinking...</span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Form Input Area */}
          <div className="border-t border-white/5 pt-4 flex gap-3">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder={`Ask about ${activeIncident?.id} logs, changes or preventions...`}
              className="flex-1 px-4 py-3 text-sm glass-input"
            />
            <button
              onClick={() => handleSendMessage(inputValue)}
              className="p-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl shadow-glow-indigo transition-all cursor-pointer"
            >
              <Send className="w-4.5 h-4.5" />
            </button>
          </div>

        </div>

        {/* Prompt Suggestions - 4 Columns */}
        <div className="lg:col-span-4 flex flex-col p-5 rounded-2xl glass-panel border border-white/5 shadow-glass h-full overflow-y-auto space-y-4">
          <h4 className="text-xs font-bold text-gray-200 uppercase tracking-wider font-mono flex items-center gap-2 pb-3 border-b border-white/5">
            <HelpCircle className="w-4.5 h-4.5 text-indigo-400" />
            <span>Interactive Suggestions</span>
          </h4>
          <p className="text-xs text-gray-400 leading-normal">
            Quickly query the AI Copilot using these context questions generated directly from this incident's telemetry:
          </p>

          <div className="flex flex-col gap-2.5">
            {suggestedQuestions.map((q) => (
              <button
                key={q}
                onClick={() => handleSendMessage(q)}
                className="w-full text-left p-3.5 text-xs font-semibold rounded-xl bg-white/5 hover:bg-indigo-600/10 border border-white/5 hover:border-indigo-500/30 text-gray-300 hover:text-indigo-200 transition-all cursor-pointer flex justify-between items-center group"
              >
                <span>{q}</span>
                <Send className="w-3.5 h-3.5 text-gray-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition-all" />
              </button>
            ))}
          </div>

          <div className="flex-1"></div>

          {/* Agent diagnostics report info */}
          <div className="p-3.5 rounded-xl bg-indigo-500/5 border border-indigo-500/10 text-[11px] text-gray-400 leading-normal space-y-1.5 font-mono">
            <div className="flex items-center gap-1.5 text-indigo-300 font-bold">
              <Terminal className="w-3.5 h-3.5" />
              <span>Copilot Engine v2.4</span>
            </div>
            <p>Knowledge Base contains compiled indices for 5 target scenarios including OOM sockets, PG connections, and gateway timeouts.</p>
          </div>
        </div>

      </div>

    </div>
  );
};

export default Copilot;
