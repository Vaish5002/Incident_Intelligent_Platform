"""
Risk Assessment and RCA Generation API Routes
"""
from fastapi import APIRouter, HTTPException
from loguru import logger

from schemas.risk import (
    RiskRequest,
    RiskResponse,
    ComprehensiveRCARequest,
    ComprehensiveRCAResponse
)
from schemas.rca import QuickRCARequest, RCAResponse
from ai.risk_engine import RiskEngine
from ai.rca_generator import RCAGenerator

router = APIRouter(prefix="/api", tags=["Risk & RCA Generation"])

# Initialize services
try:
    risk_engine = RiskEngine()
    rca_generator = RCAGenerator()
    logger.info("Risk engine and RCA generator initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    risk_engine = None
    rca_generator = None


@router.post("/risk-score", response_model=RiskResponse)
async def calculate_risk_score(request: RiskRequest):
    """
    Calculate risk score for an incident
    
    Analyzes incident data and assigns:
    - Severity level (Low/Medium/High/Critical)
    - Risk score (0-100)
    - Confidence level (0-100)
    
    **Logic:**
    - Database failures → Critical (score > 90)
    - Memory leaks → High (score 70-89)
    - Warnings → Low (score < 30)
    
    **Example:**
    ```json
    {
      "incident": "Database connection timeout",
      "logs": "Connection pool exhausted",
      "affected_service": "payment",
      "error_count": 243
    }
    ```
    
    **Returns:**
    ```json
    {
      "severity": "Critical",
      "risk_score": 91,
      "confidence": 95
    }
    ```
    """
    
    if not risk_engine:
        raise HTTPException(
            status_code=503,
            detail="Risk engine not available"
        )
    
    try:
        logger.info(f"Calculating risk for incident: {request.incident[:50]}...")
        
        result = risk_engine.calculate_risk(
            incident_description=request.incident,
            logs=request.logs,
            affected_service=request.affected_service,
            error_count=request.error_count,
            user_impact=request.user_impact,
            business_impact=request.business_impact,
            timeline_events=request.timeline_events
        )
        
        logger.info(f"Risk calculated: {result['severity']} (score: {result['risk_score']})")
        
        return RiskResponse(**result)
        
    except Exception as e:
        logger.error(f"Error calculating risk: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-comprehensive-rca", response_model=ComprehensiveRCAResponse)
async def generate_comprehensive_rca(request: ComprehensiveRCARequest):
    """
    Generate comprehensive Root Cause Analysis
    
    Combines all data sources to generate complete RCA:
    - GitHub commit analysis
    - Log analysis
    - Timeline analysis
    - Risk assessment
    - Root cause identification
    - AI-generated recommendations
    
    **Input:**
    - Incident description
    - GitHub findings (commits, changes)
    - Log findings (errors, patterns)
    - Timeline (events, sequence)
    
    **Output:**
    - Root Cause (detailed analysis)
    - Impact (user, business, system)
    - Recommendations (immediate, short-term, long-term)
    - Prevention measures
    - Risk assessment
    
    **Example:**
    ```json
    {
      "incident": "Database timeout causing payment failures",
      "github_findings": {
        "commits": [{"message": "Update DB config"}]
      },
      "log_findings": {
        "summary": "Connection pool exhausted",
        "error_count": 243
      },
      "affected_service": "payment"
    }
    ```
    """
    
    if not rca_generator:
        raise HTTPException(
            status_code=503,
            detail="RCA generator not available"
        )
    
    try:
        logger.info("Generating comprehensive RCA")
        
        result = rca_generator.generate_rca(
            incident_description=request.incident,
            github_findings=request.github_findings,
            log_findings=request.log_findings,
            timeline=request.timeline,
            affected_service=request.affected_service,
            similar_incidents=request.similar_incidents
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Failed to generate RCA")
            )
        
        logger.info("Comprehensive RCA generated successfully")
        
        return ComprehensiveRCAResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating comprehensive RCA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-quick-rca-v2", response_model=RCAResponse)
async def generate_quick_rca_v2(request: QuickRCARequest):
    """
    Generate quick RCA with risk assessment (v2)
    
    Enhanced quick RCA that includes:
    - Fast incident analysis
    - Automated risk scoring
    - Top 3 immediate actions
    - Risk level assessment
    
    Faster than comprehensive RCA, better than basic quick RCA.
    
    **Example:**
    ```json
    {
      "incident": "Payment service timeout",
      "logs": "Database connection errors",
      "timeline": "Deploy -> Error"
    }
    ```
    """
    
    if not rca_generator:
        raise HTTPException(
            status_code=503,
            detail="RCA generator not available"
        )
    
    try:
        logger.info("Generating quick RCA v2 with risk assessment")
        
        result = rca_generator.generate_quick_rca(
            incident_description=request.incident,
            logs=request.logs,
            timeline=request.timeline
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
        logger.error(f"Error generating quick RCA v2: {e}")
        raise HTTPException(status_code=500, detail=str(e))
