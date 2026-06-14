import React, { createContext, useContext, useState, useEffect } from 'react';
import { mockIncidents } from '../services/mockData';
import { api } from '../services/api';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [incidents, setIncidents] = useState(mockIncidents); // Start with mock data
  const [activeIncidentId, setActiveIncidentId] = useState("INC-3091");
  const [backendAvailable, setBackendAvailable] = useState(false);
  const [loadingInvestigations, setLoadingInvestigations] = useState(false);

  // Check backend health and load investigations on mount
  useEffect(() => {
    checkBackendAndLoadData();
  }, []);

  const checkBackendAndLoadData = async () => {
    try {
      // Check if backend is available
      const healthCheck = await api.healthCheck();
      
      if (healthCheck.success) {
        setBackendAvailable(true);
        // Load real investigations from backend
        await loadInvestigations();
      }
    } catch (error) {
      console.warn('Backend not available, using mock data:', error.message);
      setBackendAvailable(false);
    }
  };

  const loadInvestigations = async () => {
    setLoadingInvestigations(true);
    try {
      const response = await api.getInvestigations();
      
      if (response.success && response.data.length > 0) {
        // Convert backend investigations to frontend format
        const backendIncidents = response.data.map(inv => ({
          id: `INC-${inv.id}`,
          name: `INC-${inv.id}: ${inv.incident_description.substring(0, 50)}`,
          shortName: inv.incident_description.split('.')[0] || "Investigation",
          severity: inv.status === "completed" ? "MEDIUM" : "HIGH",
          status: inv.status === "completed" ? "RESOLVED" : "INVESTIGATING",
          time: new Date().toISOString().replace('T', ' ').substring(0, 19),
          riskScore: 75,
          errorCount: 0,
          category: "Backend Investigation",
          activeUsersAffected: 0,
          impactScore: 7.0,
          backendInvestigationId: inv.id,
          repo_url: inv.repo_url,
          incident_description: inv.incident_description,
          gitAnalysis: {
            repoUrl: inv.repo_url || "",
            commitHash: "N/A",
            commitUrl: "",
            author: "N/A",
            diff: "No repository changes detected.",
            riskyCodeChanges: []
          },
          logAnalysis: {
            rootCause: inv.incident_description,
            errorPatterns: [],
            errorCount: 0,
            rawLogs: ""
          },
          timelineAnalysis: {
            sequence: [],
            duration: "N/A",
            triggerType: "Manual"
          },
          riskAssessment: {
            score: 75,
            severity: "MEDIUM",
            confidence: "85%",
            riskFactors: []
          },
          aiRecommendations: []
        }));

        // Merge with mock incidents (keep mock data for demo purposes)
        setIncidents([...backendIncidents, ...mockIncidents]);
        
        // Set first backend incident as active if available
        if (backendIncidents.length > 0) {
          setActiveIncidentId(backendIncidents[0].id);
        }
      }
    } catch (error) {
      console.error('Failed to load investigations:', error);
    } finally {
      setLoadingInvestigations(false);
    }
  };

  const login = (email, password) => {
    // Basic mock verification
    if (email && password) {
      setIsAuthenticated(true);
      setUser({ email, name: "SRE Operator", role: "Incident Responder" });
      return true;
    }
    return false;
  };

  const logout = () => {
    setIsAuthenticated(false);
    setUser(null);
  };

  const activeIncident = incidents.find(inc => inc.id === activeIncidentId) || incidents[0];

  const addIncident = (newIncident) => {
    setIncidents(prev => [newIncident, ...prev]);
    setActiveIncidentId(newIncident.id);
  };

  const refreshInvestigations = async () => {
    await loadInvestigations();
  };

  return (
    <AppContext.Provider value={{
      isAuthenticated,
      user,
      incidents,
      activeIncidentId,
      activeIncident,
      setActiveIncidentId,
      login,
      logout,
      addIncident,
      backendAvailable,
      loadingInvestigations,
      refreshInvestigations
    }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
};
