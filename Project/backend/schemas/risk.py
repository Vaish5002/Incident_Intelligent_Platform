"""
Risk assessment schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class RiskRequest(BaseModel):
    """Request to calculate risk score"""
    incident: str = Field(..., description="Incident description")
    logs: Optional[str] = Field(None, description="Log summary")
    affected_service: Optional[str] = Field(None, description="Affected service")
    error_count: Optional[int] = Field(None, description="Number of errors")
    user_impact: Optional[str] = Field(None, description="User impact description")
    business_impact: Optional[str] = Field(None, description="Business impact description")
    timeline_events: Optional[List[Dict[str, Any]]] = Field(None, description="Timeline events")
    
    class Config:
        json_schema_extra = {
            "example": {
                "incident": "Database connection timeout",
                "logs": "Connection pool exhausted, timeout after 30s",
                "affected_service": "payment",
                "error_count": 243
            }
        }


class RiskResponse(BaseModel):
    """Risk assessment response"""
    severity: str = Field(..., description="Severity level (Low/Medium/High/Critical)")
    risk_score: float = Field(..., description="Risk score (0-100)")
    confidence: float = Field(..., description="Confidence in assessment (0-100)")
    breakdown: Optional[Dict[str, float]] = Field(None, description="Score breakdown")
    factors: Optional[List[str]] = Field(None, description="Risk factors identified")
    success: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "severity": "Critical",
                "risk_score": 91.5,
                "confidence": 95.0,
                "breakdown": {
                    "severity_score": 92.0,
                    "service_score": 90.0,
                    "error_score": 85.0,
                    "impact_score": 90.0,
                    "timeline_score": 70.0
                },
                "factors": [
                    "Database issues detected",
                    "Financial transaction affected",
                    "Multiple errors detected"
                ],
                "success": True
            }
        }


class ComprehensiveRCARequest(BaseModel):
    """Request for comprehensive RCA generation"""
    incident: str = Field(..., description="Incident description")
    github_findings: Optional[Dict[str, Any]] = Field(None, description="GitHub analysis")
    log_findings: Optional[Dict[str, Any]] = Field(None, description="Log analysis")
    timeline: Optional[Dict[str, Any]] = Field(None, description="Timeline data")
    affected_service: Optional[str] = Field(None, description="Affected service")
    similar_incidents: Optional[str] = Field(None, description="Similar past incidents")
    
    class Config:
        json_schema_extra = {
            "example": {
                "incident": "Users unable to complete payment transactions",
                "github_findings": {
                    "repo_name": "company/payment-service",
                    "commits": [
                        {
                            "sha": "abc123",
                            "message": "Update database pool configuration",
                            "changed_files": ["config/database.py"]
                        }
                    ]
                },
                "log_findings": {
                    "summary": "Database timeout errors, connection pool exhausted",
                    "error_count": 243,
                    "critical_errors": [
                        {"message": "Connection timeout after 30s"}
                    ]
                },
                "affected_service": "payment"
            }
        }


class ComprehensiveRCAResponse(BaseModel):
    """Comprehensive RCA response"""
    success: bool
    rca_text: str = Field(..., description="Generated RCA in markdown format")
    risk_assessment: Dict[str, Any] = Field(..., description="Risk assessment data")
    root_cause_candidates: List[Dict[str, Any]] = Field(..., description="Identified root causes")
    model_used: Optional[str] = Field(None, description="AI model used")
    metadata: Dict[str, Any] = Field(..., description="Incident metadata")
    error: Optional[str] = None
    
    class Config:
        protected_namespaces = ()  # Allow model_used field
        json_schema_extra = {
            "example": {
                "success": True,
                "rca_text": "## Root Cause Analysis\n\n### Executive Summary\n...",
                "risk_assessment": {
                    "severity": "Critical",
                    "risk_score": 91.5,
                    "confidence": 95.0
                },
                "root_cause_candidates": [
                    {
                        "type": "code_change",
                        "confidence": 0.85,
                        "description": "Database pool size reduced in recent commit"
                    }
                ],
                "model_used": "gemini-flash-latest",
                "metadata": {
                    "incident": "Payment failures",
                    "severity": "Critical",
                    "risk_score": 91.5
                }
            }
        }
