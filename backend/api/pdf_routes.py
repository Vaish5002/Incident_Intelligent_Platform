"""
PDF Generation API Routes
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from loguru import logger
from datetime import datetime

from backend.ai.pdf_generator import PDFGenerator
from backend.ai.knowledge_base import KnowledgeBaseService

router = APIRouter(prefix="/api/pdf", tags=["PDF Generation"])

# Initialize services
try:
    pdf_generator = PDFGenerator()
    kb_service = KnowledgeBaseService()
    logger.info("PDF generator initialized for API")
except Exception as e:
    logger.error(f"Failed to initialize PDF generator: {e}")
    pdf_generator = None
    kb_service = None


# Request/Response Models
class GeneratePDFRequest(BaseModel):
    """Request for generating RCA PDF"""
    incident_id: str
    incident_description: str
    rca_text: str
    severity: str
    risk_score: float
    confidence: float
    affected_service: str
    occurred_at: Optional[str] = None
    resolved_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class GenerateSummaryPDFRequest(BaseModel):
    """Request for generating summary PDF"""
    title: Optional[str] = "Incident Summary Report"
    incident_ids: Optional[List[str]] = None  # If provided, only these incidents
    severity: Optional[str] = None  # Filter by severity
    limit: Optional[int] = 50  # Maximum incidents to include


@router.post("/generate-rca")
async def generate_rca_pdf(request: GeneratePDFRequest):
    """
    Generate PDF report for RCA
    
    **Test 1 Requirement:** Generate PDF → PDF downloads successfully
    
    Contents:
    - Executive Summary
    - Timeline
    - Root Cause
    - Severity & Risk Score
    - Recommendations
    - Prevention Plan
    
    Example:
    ```json
    {
      "incident_id": "INC-2024-001",
      "incident_description": "Payment service failures",
      "rca_text": "## Executive Summary\\n...",
      "severity": "Critical",
      "risk_score": 85.5,
      "confidence": 90.0,
      "affected_service": "payment",
      "occurred_at": "2024-01-15T10:30:00",
      "resolved_at": "2024-01-15T12:45:00"
    }
    ```
    
    Returns:
    - PDF file download
    """
    if not pdf_generator or not pdf_generator.is_available():
        raise HTTPException(
            status_code=503,
            detail="PDF generation not available. Install reportlab: pip install reportlab"
        )
    
    try:
        logger.info(f"Generating PDF for incident {request.incident_id}")
        
        # Generate PDF
        pdf_buffer = pdf_generator.generate_rca_pdf(
            incident_id=request.incident_id,
            incident_description=request.incident_description,
            rca_text=request.rca_text,
            severity=request.severity,
            risk_score=request.risk_score,
            confidence=request.confidence,
            affected_service=request.affected_service,
            occurred_at=request.occurred_at,
            resolved_at=request.resolved_at,
            metadata=request.metadata
        )
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"RCA_{request.incident_id}_{timestamp}.pdf"
        
        logger.info(f"PDF generated successfully: {filename}")
        
        # Return PDF as downloadable file
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/generate-from-incident/{incident_id}")
async def generate_pdf_from_incident(incident_id: str):
    """
    Generate PDF report from stored incident
    
    Retrieves incident and RCA from knowledge base and generates PDF.
    
    Example: GET /api/pdf/generate-from-incident/INC-2024-001
    
    Returns:
    - PDF file download
    """
    if not pdf_generator or not pdf_generator.is_available():
        raise HTTPException(
            status_code=503,
            detail="PDF generation not available. Install reportlab: pip install reportlab"
        )
    
    if not kb_service:
        raise HTTPException(status_code=503, detail="Knowledge base service not available")
    
    try:
        # Get incident from knowledge base
        incident = kb_service.get_incident(incident_id)
        
        if not incident:
            raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
        
        # Check if RCA report exists
        if not incident.get('rca_report'):
            raise HTTPException(
                status_code=404,
                detail=f"RCA report not found for incident {incident_id}"
            )
        
        rca = incident['rca_report']
        
        # Generate PDF
        pdf_buffer = pdf_generator.generate_rca_pdf(
            incident_id=incident['incident_id'],
            incident_description=incident['description'],
            rca_text=rca['rca_text'],
            severity=incident['severity'],
            risk_score=incident['risk_score'],
            confidence=incident['confidence'],
            affected_service=incident['affected_service'],
            occurred_at=incident.get('occurred_at'),
            resolved_at=incident.get('resolved_at')
        )
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"RCA_{incident_id}_{timestamp}.pdf"
        
        logger.info(f"PDF generated from stored incident: {filename}")
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF from incident: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-summary")
async def generate_summary_pdf(request: GenerateSummaryPDFRequest):
    """
    Generate summary PDF for multiple incidents
    
    **Test 2 Requirement:** Large RCA → Formatting remains correct
    
    Creates a summary report with table of incidents.
    
    Example:
    ```json
    {
      "title": "Monthly Incident Report",
      "severity": "Critical",
      "limit": 50
    }
    ```
    
    Returns:
    - PDF file download with incident summary
    """
    if not pdf_generator or not pdf_generator.is_available():
        raise HTTPException(
            status_code=503,
            detail="PDF generation not available. Install reportlab: pip install reportlab"
        )
    
    if not kb_service:
        raise HTTPException(status_code=503, detail="Knowledge base service not available")
    
    try:
        # Get incidents from knowledge base
        if request.incident_ids:
            # Get specific incidents
            incidents = []
            for incident_id in request.incident_ids:
                incident = kb_service.get_incident(incident_id)
                if incident:
                    incidents.append(incident)
        else:
            # Get all incidents with filters
            incidents = kb_service.get_all_incidents(
                limit=request.limit,
                severity=request.severity
            )
        
        if not incidents:
            raise HTTPException(status_code=404, detail="No incidents found")
        
        # Generate summary PDF
        pdf_buffer = pdf_generator.generate_summary_pdf(
            incidents=incidents,
            title=request.title
        )
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Incident_Summary_{timestamp}.pdf"
        
        logger.info(f"Summary PDF generated: {filename} ({len(incidents)} incidents)")
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating summary PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_pdf_info():
    """
    Get PDF generator service information
    
    Returns service status and capabilities.
    """
    if not pdf_generator:
        return {
            "service": "PDF Generator",
            "status": "unavailable",
            "error": "Service not initialized"
        }
    
    try:
        info = pdf_generator.get_service_info()
        return info
        
    except Exception as e:
        logger.error(f"Error getting PDF info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def pdf_health_check():
    """
    Health check for PDF generator service
    """
    if not pdf_generator:
        return {
            "status": "unhealthy",
            "service": "PDF Generator",
            "error": "Service not initialized"
        }
    
    try:
        available = pdf_generator.is_available()
        return {
            "status": "healthy" if available else "unavailable",
            "service": "PDF Generator",
            "available": available,
            "library": "reportlab" if available else "not installed"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "PDF Generator",
            "error": str(e)
        }
