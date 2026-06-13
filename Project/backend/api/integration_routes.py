"""
Member 1 Integration API Routes
Endpoints for consuming Member 1 data and processing through Member 3 engines
"""
from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import Optional

from ai.member1_integration import Member1IntegrationService
from ai.groq_service import GroqService
from ai.risk_engine import RiskEngine
from ai.rag_service import RAGService

router = APIRouter(prefix="/api/integration", tags=["Member 1 Integration"])

# Initialize services
try:
    member1_service = Member1IntegrationService()
    groq_service = GroqService()
    risk_engine = RiskEngine()
    rag_service = RAGService()
    logger.info("Integration services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize integration services: {e}")
    member1_service = None


@router.get("/health")
async def health_check():
    """
    Health check for integration service
    """
    if not member1_service:
        return {
            "status": "unavailable",
            "service": "Member 1 Integration",
            "error": "Service not initialized"
        }
    
    member1_health = member1_service.check_member1_health()
    
    return {
        "status": "healthy" if member1_health.get("available") else "degraded",
        "service": "Member 1 Integration",
        "member1_status": member1_health
    }


@router.get("/info")
async def service_info():
    """
    Get service information
    """
    if not member1_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    return member1_service.get_service_info()


@router.get("/investigation/{investigation_id}")
async def get_investigation_data(investigation_id: int):
    """
    Get investigation data from Member 1
    
    Args:
        investigation_id: Investigation ID
        
    Returns:
        Raw investigation data from Member 1
    """
    if not member1_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        logger.info(f"Fetching investigation {investigation_id} from Member 1")
        
        data = member1_service.get_investigation(investigation_id)
        
        return {
            "success": True,
            "investigation_id": investigation_id,
            "data": data
        }
        
    except ValueError as e:
        logger.error(f"Investigation not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeline/{investigation_id}")
async def get_timeline_data(investigation_id: int):
    """
    Get timeline data from Member 1
    
    Args:
        investigation_id: Investigation ID
        
    Returns:
        Timeline data from Member 1
    """
    if not member1_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        logger.info(f"Fetching timeline for investigation {investigation_id}")
        
        data = member1_service.get_timeline(investigation_id)
        
        return {
            "success": True,
            "investigation_id": investigation_id,
            "timeline": data
        }
        
    except ValueError as e:
        logger.error(f"Timeline not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-full/{investigation_id}")
async def process_investigation_full(
    investigation_id: int,
    generate_rca: bool = True,
    calculate_risk: bool = True,
    find_similar: bool = True
):
    """
    Full integration pipeline: Get data from Member 1 and process through all engines
    
    This endpoint:
    1. Fetches investigation data from Member 1
    2. Fetches timeline data from Member 1
    3. Extracts data for RCA Engine
    4. Extracts data for Risk Engine
    5. Extracts data for RAG System
    6. Optionally generates RCA, calculates risk, finds similar incidents
    
    Args:
        investigation_id: Investigation ID from Member 1
        generate_rca: Generate AI-powered RCA
        calculate_risk: Calculate risk score
        find_similar: Find similar incidents
        
    Returns:
        Complete processing results with RCA, risk score, and similar incidents
    """
    if not member1_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        logger.info(f"Starting full processing for investigation {investigation_id}")
        
        # Step 1: Get data from Member 1 and prepare for engines
        results = member1_service.process_investigation_full(
            investigation_id=investigation_id,
            generate_rca=generate_rca,
            calculate_risk=calculate_risk,
            find_similar=find_similar
        )
        
        # Step 2: Generate RCA if requested
        if generate_rca and groq_service:
            try:
                rca_input = results['processing']['rca_input']
                
                logger.info("Generating RCA with Groq AI...")
                rca_result = groq_service.generate_rca(
                    incident_description=rca_input.get('incident', ''),
                    severity=rca_input.get('severity', 'medium'),
                    affected_service=rca_input.get('affected_service', 'unknown'),
                    risk_score=50.0,  # Will be calculated next
                    github_analysis=rca_input.get('github_analysis', {}),
                    log_analysis=rca_input.get('log_analysis', {}),
                    timeline={"events": rca_input.get('timeline', [])},
                    root_cause_candidates=rca_input.get('root_cause_candidates', [])
                )
                
                results['rca'] = rca_result
                logger.info("✅ RCA generated successfully")
                
            except Exception as e:
                logger.error(f"RCA generation failed: {e}")
                results['rca'] = {"success": False, "error": str(e)}
        
        # Step 3: Calculate risk if requested
        if calculate_risk and risk_engine:
            try:
                risk_input = results['processing']['risk_input']
                
                logger.info("Calculating risk score...")
                risk_result = risk_engine.calculate_risk_score(
                    incident_description=risk_input.get('incident_description', ''),
                    severity=risk_input.get('severity', 'medium'),
                    affected_service=risk_input.get('affected_service', 'unknown'),
                    error_count=risk_input.get('error_count', 0),
                    incident_type=risk_input.get('incident_type', 'Unknown')
                )
                
                results['risk_assessment'] = risk_result
                logger.info("✅ Risk calculated successfully")
                
            except Exception as e:
                logger.error(f"Risk calculation failed: {e}")
                results['risk_assessment'] = {"error": str(e)}
        
        # Step 4: Find similar incidents if requested
        if find_similar and rag_service:
            try:
                rag_input = results['processing']['rag_input']
                
                logger.info("Finding similar incidents...")
                similar_result = rag_service.find_similar_incidents(
                    incident_description=rag_input.get('incident_description', ''),
                    top_k=5
                )
                
                results['similar_incidents'] = similar_result
                logger.info("✅ Similar incidents found")
                
            except Exception as e:
                logger.error(f"RAG search failed: {e}")
                results['similar_incidents'] = {"success": False, "error": str(e)}
        
        logger.info(f"✅ Full processing completed for investigation {investigation_id}")
        
        return {
            "success": True,
            "investigation_id": investigation_id,
            "results": results
        }
        
    except ValueError as e:
        logger.error(f"Investigation not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Error in full processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-for-rca/{investigation_id}")
async def extract_for_rca(investigation_id: int):
    """
    Get investigation data and extract for RCA Engine
    
    Returns data formatted for RCA generation
    """
    if not member1_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        data = member1_service.get_investigation(investigation_id)
        rca_input = member1_service.extract_for_rca(data)
        
        return {
            "success": True,
            "investigation_id": investigation_id,
            "rca_input": rca_input
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-for-risk/{investigation_id}")
async def extract_for_risk(investigation_id: int):
    """
    Get investigation data and extract for Risk Engine
    
    Returns data formatted for risk scoring
    """
    if not member1_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        data = member1_service.get_investigation(investigation_id)
        risk_input = member1_service.extract_for_risk_engine(data)
        
        return {
            "success": True,
            "investigation_id": investigation_id,
            "risk_input": risk_input
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-for-rag/{investigation_id}")
async def extract_for_rag(investigation_id: int):
    """
    Get investigation data and extract for RAG System
    
    Returns data formatted for similarity search
    """
    if not member1_service:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        data = member1_service.get_investigation(investigation_id)
        rag_input = member1_service.extract_for_rag(data)
        
        return {
            "success": True,
            "investigation_id": investigation_id,
            "rag_input": rag_input
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
