"""
RCA-related schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class RCARequest(BaseModel):
    """Request to generate RCA"""
    incident: str = Field(..., description="Incident description")
    logs: str = Field(..., description="Log summary or full logs")
    timeline: str = Field(..., description="Timeline of events")
    severity: Optional[str] = Field("medium", description="Incident severity")
    affected_service: Optional[str] = Field("unknown", description="Affected service")
    risk_score: Optional[float] = Field(50.0, description="Risk score (0-100)")
    github_analysis: Optional[Dict[str, Any]] = Field(None, description="GitHub analysis data")
    log_analysis: Optional[Dict[str, Any]] = Field(None, description="Log analysis data")
    timeline_data: Optional[Dict[str, Any]] = Field(None, description="Timeline data")
    root_cause_candidates: Optional[List[Dict[str, Any]]] = Field(None, description="Root cause candidates")
    
    class Config:
        json_schema_extra = {
            "example": {
                "incident": "Users cannot complete payments after deployment",
                "logs": "Database timeout, Pool exhausted, Payment service failed",
                "timeline": "Deployment started -> Config changed -> Database timeout -> Payment failure",
                "severity": "critical",
                "affected_service": "payment",
                "risk_score": 91.0
            }
        }


class RCAResponse(BaseModel):
    """RCA generation response"""
    incident_id: Optional[str] = None
    rca_text: str
    model_used: Optional[str] = None
    success: bool
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "incident_id": "INC-12345678",
                "rca_text": "## Root Cause Analysis\n\n### Executive Summary\nThe payment service failure was caused by...",
                "model_used": "gemini-1.5-flash",
                "success": True
            }
        }


class QuickRCARequest(BaseModel):
    """Quick RCA request (simplified)"""
    incident: str
    logs: str
    timeline: str


class RecommendationRequest(BaseModel):
    """Request to generate recommendations"""
    root_cause: str
    severity: str
    affected_service: str


class RecommendationResponse(BaseModel):
    """Recommendations response"""
    recommendations: str
    success: bool
    error: Optional[str] = None
