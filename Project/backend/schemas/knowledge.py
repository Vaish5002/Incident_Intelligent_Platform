"""
Knowledge Base and Embedding Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class IncidentCreate(BaseModel):
    """Create incident request"""
    incident_id: str = Field(..., description="Unique incident ID")
    description: str = Field(..., description="Incident description")
    severity: str = Field(..., description="Severity level")
    affected_service: str = Field(..., description="Affected service")
    risk_score: float = Field(..., description="Risk score (0-100)")
    confidence: float = Field(..., description="Confidence (0-100)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "incident_id": "INC-2024-001",
                "description": "Database connection timeout",
                "severity": "Critical",
                "affected_service": "payment",
                "risk_score": 85.0,
                "confidence": 90.0
            }
        }


class RCAReportCreate(BaseModel):
    """Create RCA report request"""
    incident_id: str
    root_cause: str
    impact_analysis: str
    recommendations: str
    prevention_measures: str
    rca_text: str
    model_used: str
    root_cause_candidates: Optional[List[Dict[str, Any]]] = None


class KnowledgeEntryCreate(BaseModel):
    """Create knowledge entry request"""
    incident_id: str
    entry_type: str = Field(..., description="Entry type (incident_description, root_cause, fix, recommendation)")
    title: str
    content: str
    tags: Optional[List[str]] = None


class IncidentResponse(BaseModel):
    """Incident response"""
    incident_id: str
    description: str
    severity: str
    affected_service: str
    status: str
    risk_score: Optional[float]
    confidence: Optional[float]
    occurred_at: Optional[str]
    resolved_at: Optional[str]
    rca_report: Optional[Dict[str, Any]] = None


class EmbeddingRequest(BaseModel):
    """Generate embedding request"""
    text: str = Field(..., description="Text to embed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Database connection timeout causing payment failures"
            }
        }


class EmbeddingBatchRequest(BaseModel):
    """Generate embeddings for multiple texts"""
    texts: List[str] = Field(..., description="List of texts to embed")


class EmbeddingResponse(BaseModel):
    """Embedding response"""
    embedding: List[float] = Field(..., description="Embedding vector")
    dimensions: int = Field(..., description="Number of dimensions")
    model: str = Field(..., description="Model used")
    success: bool = True


class SimilarityRequest(BaseModel):
    """Calculate similarity request"""
    embedding1: List[float]
    embedding2: List[float]


class SimilarityResponse(BaseModel):
    """Similarity response"""
    similarity: float = Field(..., description="Similarity score (0.0 to 1.0)")
    success: bool = True


class SearchRequest(BaseModel):
    """Search knowledge base request"""
    query: str = Field(..., description="Search query")
    entry_type: Optional[str] = Field(None, description="Filter by entry type")
    limit: int = Field(10, description="Maximum results")


class SearchResponse(BaseModel):
    """Search response"""
    results: List[Dict[str, Any]]
    count: int
    success: bool = True
