import React, { createContext, useContext, useState } from 'react';
import { mockIncidents } from '../services/mockData';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [incidents, setIncidents] = useState(mockIncidents);
  const [activeIncidentId, setActiveIncidentId] = useState("INC-3091");

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
      addIncident
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
