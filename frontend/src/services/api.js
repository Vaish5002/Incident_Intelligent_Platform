// Mock API endpoints to simulate backend integration for SmartOps AI
import { mockIncidents } from './mockData';

// Helper to simulate network latency
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const api = {
  /**
   * POST /investigate
   * Triggers analysis with repository information and description
   */
  investigate: async (githubUrl, description) => {
    await delay(1200);
    // Find or create a matching template based on keyword search
    const query = (githubUrl + ' ' + description).toLowerCase();
    let matchedTemplate = mockIncidents[0]; // Default to DB Timeout

    if (query.includes('gateway') || query.includes('kong')) {
      matchedTemplate = mockIncidents[1];
    } else if (query.includes('null') || query.includes('pointer') || query.includes('auth')) {
      matchedTemplate = mockIncidents[2];
    } else if (query.includes('memory') || query.includes('leak') || query.includes('websocket') || query.includes('oom')) {
      matchedTemplate = mockIncidents[3];
    } else if (query.includes('stripe') || query.includes('payment') || query.includes('checkout')) {
      matchedTemplate = mockIncidents[4];
    }

    // Return a mock investigation task registration response
    return {
      success: true,
      taskId: `task-${Math.floor(Math.random() * 90000) + 10000}`,
      message: "Investigation analysis successfully registered.",
      templateId: matchedTemplate.id
    };
  },

  /**
   * POST /upload-log
   * Simulates uploading a raw log file to the analyzer engine
   */
  uploadLog: async (file) => {
    await delay(1000);
    if (!file) {
      throw new Error("No file uploaded");
    }
    return {
      success: true,
      filename: file.name,
      size: file.size,
      message: "Log file successfully uploaded and indexed."
    };
  },

  /**
   * GET /results/:id
   * Resolves detailed multi-agent findings for a completed investigation
   */
  getResults: async (id) => {
    await delay(800);
    const result = mockIncidents.find((inc) => inc.id === id);
    if (!result) {
      throw new Error(`Investigation results for target ID ${id} not found.`);
    }
    return {
      success: true,
      data: result
    };
  },

  /**
   * GET /download-pdf/:id
   * Resolves PDF download streams or opens printable PDF views
   */
  downloadPdf: async (id) => {
    await delay(1500);
    const result = mockIncidents.find((inc) => inc.id === id);
    if (!result) {
      throw new Error(`Report for target ID ${id} not found.`);
    }
    
    // Simulate blob stream payload
    return {
      success: true,
      filename: `RCA_Report_${id}.pdf`,
      downloadUrl: `#pdf-download-simulated-${id}`
    };
  }
};
