// Real API endpoints for SmartOps AI Backend Integration
import axios from 'axios';

// Backend API URLs - Use environment variable or fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002';
const MEMBER1_API_URL = import.meta.env.VITE_MEMBER1_API_URL || 'http://localhost:8000'; // Member 1 - Investigation Backend
const MEMBER3_API_URL = `${API_BASE_URL}/api`; // Member 3 - AI/RCA Engine

// Configure axios defaults
axios.defaults.timeout = 30000; // 30 second timeout
axios.defaults.headers.common['Content-Type'] = 'application/json';

export const api = {
  /**
   * POST /investigate
   * Triggers full investigation - automatically fetches logs from Chaos Platform
   */
  investigate: async (githubUrl, description) => {
    try {
      const response = await axios.post(`${MEMBER3_API_URL}/investigate`, {
        repo_url: githubUrl,
        incident_description: description
      });

      return {
        success: true,
        investigationId: response.data.investigation_id,
        status: response.data.status,
        message: "Investigation started successfully",
        data: response.data
      };
    } catch (error) {
      console.error('Investigation API error:', error);
      throw new Error(error.response?.data?.detail || error.message || 'Failed to start investigation');
    }
  },

  /**
   * POST /upload-log
   * Uploads log file (currently not used by backend, but kept for frontend compatibility)
   */
  uploadLog: async (file) => {
    // Note: Backend fetches logs from Project 2, not via file upload
    // This is kept for UI compatibility
    return {
      success: true,
      filename: file?.name || 'logs.txt',
      size: file?.size || 0,
      message: "Log analysis will be performed from Project 2 API"
    };
  },

  /**
   * GET /investigations
   * Get all investigations
   */
  getInvestigations: async () => {
    try {
      const response = await axios.get(`${MEMBER1_API_URL}/investigations`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Get investigations error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to fetch investigations');
    }
  },

  /**
   * GET /investigations/:id
   * Get complete investigation results including analysis
   */
  getResults: async (id) => {
    try {
      // Try demo endpoint first (Member 3 API on port 8002)
      const response = await axios.get(`${MEMBER3_API_URL}/investigations/${id}`);
      
      if (response.data.error) {
        throw new Error(response.data.error);
      }

      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Get results error:', error);
      throw new Error(error.response?.data?.detail || error.message || 'Failed to fetch investigation results');
    }
  },

  /**
   * GET /timeline/:id
   * Get investigation timeline with all events
   */
  getTimeline: async (id) => {
    try {
      const response = await axios.get(`${MEMBER1_API_URL}/timeline/${id}`);
      
      if (response.data.error) {
        throw new Error(response.data.error);
      }

      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Get timeline error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to fetch timeline');
    }
  },

  /**
   * GET /logs
   * Fetch logs from Project 2 or fallback data
   */
  getLogs: async () => {
    try {
      const response = await axios.get(`${MEMBER1_API_URL}/logs`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Get logs error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to fetch logs');
    }
  },

  /**
   * GET /failures
   * Get failure events from Project 2
   */
  getFailures: async () => {
    try {
      const response = await axios.get(`${MEMBER1_API_URL}/failures`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Get failures error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to fetch failures');
    }
  },

  /**
   * GET /project2-status
   * Check Project 2 (Chaos Demo) status
   */
  getProject2Status: async () => {
    try {
      const response = await axios.get(`${MEMBER1_API_URL}/project2-status`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Get Project 2 status error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to check Project 2 status');
    }
  },

  /**
   * POST /api/generate-rca (Member 3)
   * Generate AI-powered RCA report
   */
  generateRCA: async (incidentData) => {
    try {
      const response = await axios.post(`${MEMBER3_API_URL}/generate-rca`, incidentData);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Generate RCA error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to generate RCA');
    }
  },

  /**
   * POST /api/quick-rca (Member 3)
   * Generate quick RCA analysis
   */
  quickRCA: async (incident, logs) => {
    try {
      const response = await axios.post(`${MEMBER3_API_URL}/quick-rca`, {
        incident,
        logs
      });
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Quick RCA error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to generate quick RCA');
    }
  },

  /**
   * GET /api/knowledge/incidents (Member 3)
   * Get knowledge base incidents
   */
  getKnowledgeIncidents: async () => {
    try {
      const response = await axios.get(`${MEMBER3_API_URL}/knowledge/incidents`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Get knowledge incidents error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to fetch knowledge incidents');
    }
  },

  /**
   * POST /api/copilot/ask (Member 3)
   * Ask AI Copilot a question
   */
  askCopilot: async (question, context = {}) => {
    try {
      const response = await axios.post(`${MEMBER3_API_URL}/copilot/ask`, {
        question,
        context
      });
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Ask Copilot error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to get copilot response');
    }
  },

  /**
   * GET /api/pdf/generate-from-incident/:id (Member 3)
   * Download PDF report for an incident
   */
  downloadPdf: async (id) => {
    try {
      const response = await axios.get(`${MEMBER3_API_URL}/pdf/generate-from-incident/${id}`, {
        responseType: 'blob' // Important for file download
      });

      // Create blob URL and trigger download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `RCA_Report_${id}_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      return {
        success: true,
        filename: link.download,
        message: 'PDF downloaded successfully'
      };
    } catch (error) {
      console.error('Download PDF error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to download PDF report');
    }
  },

  /**
   * POST /full-investigate
   * FULL INVESTIGATION - Uses BOTH GitHub Agent AND Log Agent
   * This is the REAL implementation with all agents working
   */
  fullInvestigate: async (githubUrl, description) => {
    try {
      const response = await axios.post(`${MEMBER3_API_URL}/full-investigate`, {
        repo_url: githubUrl,
        incident_description: description
      });

      return {
        success: true,
        investigationId: response.data.investigation_id,
        status: response.data.status,
        message: "Full investigation started - all agents activated",
        data: response.data
      };
    } catch (error) {
      console.error('Full Investigation API error:', error);
      throw new Error(error.response?.data?.detail || error.message || 'Failed to start full investigation');
    }
  },

  /**
   * GET /full-investigations/:id
   * Get FULL investigation results with REAL agent data
   */
  getFullResults: async (id) => {
    try {
      const response = await axios.get(`${MEMBER3_API_URL}/full-investigations/${id}`);
      
      if (response.data.error) {
        throw new Error(response.data.error);
      }

      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Get full results error:', error);
      throw new Error(error.response?.data?.detail || error.message || 'Failed to fetch full investigation results');
    }
  },

  /**
   * GET /health (Member 1)
   * Health check for Member 1 backend
   */
  healthCheck: async () => {
    try {
      const response = await axios.get(`${MEMBER1_API_URL}/health`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Health check error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  },

  /**
   * GET /api/health (Member 3)
   * Health check for Member 3 AI/RCA Engine
   */
  member3HealthCheck: async () => {
    try {
      const response = await axios.get(`${MEMBER3_API_URL}/health`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Member 3 health check error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  },

  /**
   * POST /api/chaos/inject-failure (Member 3)
   * Proxy failure injection to Chaos Platform
   */
  injectFailure: async (type) => {
    try {
      const response = await axios.post(`${MEMBER3_API_URL}/chaos/inject-failure`, {
        type,
        duration_seconds: 300
      });
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Inject failure error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to inject failure');
    }
  }
};
