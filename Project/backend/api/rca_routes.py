"""
RCA API Routes
"""
from fastapi import APIRouter, HTTPException
from loguru import logger

from backend.schemas.rca import (
    RCARequest,
    RCAResponse,
    QuickRCARequest,
    RecommendationRequest,
    RecommendationResponse
)
from backend.ai.gemini_service import GeminiService
from backend.ai.config import settings

router = APIRouter(prefix="/api", tags=["RCA Generation"])

# Initialize Gemini service
try:
    gemini_service = GeminiService()
    logger.info("Gemini service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini service: {e}")
    gemini_service = None


@router.post("/generate-rca", response_model=RCAResponse)
async def generate_rca(request: RCARequest):
    """
    Generate comprehensive Root Cause Analysis (RCA)
    
    This endpoint accepts incident data and generates a detailed RCA using Gemini AI.
    
    **Input:**
    - incident: Description of what happened
    - logs: Log summary or full log data
    - timeline: Timeline of events
    - severity: Incident severity (optional)
    - affected_service: Service affected (optional)
    - risk_score: Risk score 0-100 (optional)
    - github_analysis: GitHub analysis data (optional)
    - log_analysis: Detailed log analysis (optional)
    - timeline_data: Structured timeline data (optional)
    - root_cause_candidates: Pre-analyzed candidates (optional)
    
    **Output:**
    - rca_text: Generated RCA in markdown format
    - model_used: AI model used
    - success: Whether generation succeeded
    """
    
    if not gemini_service:
        raise HTTPException(
            status_code=503,
            detail="Gemini service not available. Check GEMINI_API_KEY configuration."
        )
    
    try:
        logger.info(f"Generating RCA for incident: {request.incident[:50]}...")
        
        # Use provided data or fallback to simple strings
        github_data = request.github_analysis or {"repo_name": "Unknown", "commits": []}
        log_data = request.log_analysis or {"total_logs": 0, "log_summary": request.logs}
        timeline_data = request.timeline_data or {"events": [], "summary": request.timeline}
        candidates = request.root_cause_candidates or []
        
        # Generate RCA
        result = gemini_service.generate_rca(
            incident_description=request.incident,
            severity=request.severity or "medium",
            affected_service=request.affected_service or "unknown",
            risk_score=request.risk_score or 50.0,
            github_analysis=github_data,
            log_analysis=log_data,
            timeline=timeline_data,
            root_cause_candidates=candidates
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Failed to generate RCA")
            )
        
        logger.info("RCA generated successfully")
        
        return RCAResponse(
            rca_text=result["rca_text"],
            model_used=result.get("model_used"),
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating RCA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quick-rca", response_model=RCAResponse)
async def generate_quick_rca(request: QuickRCARequest):
    """
    Generate quick RCA (simplified, faster analysis)
    
    Use this for rapid incident triage when you need fast insights.
    """
    
    if not gemini_service:
        raise HTTPException(
            status_code=503,
            detail="Gemini service not available"
        )
    
    try:
        logger.info("Generating quick RCA")
        
        result = gemini_service.generate_quick_rca(
            incident_description=request.incident,
            log_summary=request.logs,
            timeline_summary=request.timeline
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Failed to generate quick RCA")
            )
        
        return RCAResponse(
            rca_text=result["rca_text"],
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating quick RCA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommendations", response_model=RecommendationResponse)
async def generate_recommendations(request: RecommendationRequest):
    """
    Generate actionable recommendations based on root cause
    
    Provides immediate, short-term, and long-term action items.
    """
    
    if not gemini_service:
        raise HTTPException(
            status_code=503,
            detail="Gemini service not available"
        )
    
    try:
        logger.info("Generating recommendations")
        
        result = gemini_service.generate_recommendations(
            root_cause=request.root_cause,
            severity=request.severity,
            affected_service=request.affected_service
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Failed to generate recommendations")
            )
        
        return RecommendationResponse(
            recommendations=result["recommendations"],
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check for RCA service"""
    
    gemini_status = "healthy" if gemini_service else "unavailable"
    api_key_configured = bool(settings.GEMINI_API_KEY)
    
    return {
        "status": "healthy" if gemini_service else "degraded",
        "service": "SmartOps AI - RCA Engine",
        "gemini_service": gemini_status,
        "gemini_api_key_configured": api_key_configured,
        "model": settings.GEMINI_MODEL
    }
