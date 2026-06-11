"""
RAG Retrieval API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger

from backend.ai.rag_service import RAGService

router = APIRouter(prefix="/api/rag", tags=["RAG Retrieval"])

# Initialize RAG service
try:
    rag_service = RAGService()
    logger.info("RAG service initialized for API")
except Exception as e:
    logger.error(f"Failed to initialize RAG service: {e}")
    rag_service = None


# Request/Response Models
class SimilarIncidentRequest(BaseModel):
    """Request for finding similar incidents"""
    incident_description: str
    logs: Optional[str] = None
    top_k: int = 5
    similarity_threshold: float = 0.3


class RAGContextRequest(BaseModel):
    """Request for RAG context"""
    incident_description: str
    logs: Optional[str] = None
    github_data: Optional[Dict[str, Any]] = None
    timeline: Optional[str] = None


class StoreSimilarityRequest(BaseModel):
    """Request to store similarity relationship"""
    source_incident_id: str
    similar_incident_id: str
    similarity_score: float
    method: str = "embedding"


@router.post("/find-similar")
async def find_similar_incidents(request: SimilarIncidentRequest):
    """
    Find similar historical incidents
    
    **Test 1 Requirement:** Known incident → Relevant match returned
    
    Flow:
    - New Incident → Embedding → Similarity Search → Top Matches
    
    Example:
    ```json
    {
      "incident_description": "Database connection timeout causing payment failures",
      "logs": "Connection pool exhausted, 500 errors",
      "top_k": 5,
      "similarity_threshold": 0.3
    }
    ```
    
    Output Example:
    ```json
    {
      "success": true,
      "similar_incidents": [
        {
          "incident_id": "INC-2024-001",
          "description": "Database timeout in payment service",
          "similarity": 89.5,
          "severity": "Critical",
          "rca_summary": {...}
        }
      ],
      "count": 1,
      "top_similarity": 89.5
    }
    ```
    """
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG service not available")
    
    try:
        result = rag_service.find_similar_incidents(
            incident_description=request.incident_description,
            logs=request.logs,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error finding similar incidents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retrieve-and-augment")
async def retrieve_and_augment(request: RAGContextRequest):
    """
    Complete RAG workflow: Retrieve + Augment
    
    Finds similar incidents and builds augmented context for AI generation.
    
    Returns:
    - Similar incidents
    - Formatted RAG context
    - Augmented prompt data
    """
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG service not available")
    
    try:
        result = rag_service.retrieve_and_augment(
            incident_description=request.incident_description,
            logs=request.logs,
            github_data=request.github_data,
            timeline=request.timeline
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in RAG workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-context")
async def get_rag_context(request: SimilarIncidentRequest):
    """
    Get formatted RAG context for AI prompts
    
    Returns markdown-formatted context from similar incidents.
    Useful for augmenting prompts with historical knowledge.
    """
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG service not available")
    
    try:
        context = rag_service.get_rag_context(
            incident_description=request.incident_description,
            logs=request.logs,
            top_k=request.top_k
        )
        
        return {
            "success": True,
            "context": context
        }
        
    except Exception as e:
        logger.error(f"Error getting RAG context: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/store-similarity")
async def store_similarity_relationship(request: StoreSimilarityRequest):
    """
    Store a similar incident relationship
    
    Records that two incidents are similar for future reference.
    """
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG service not available")
    
    try:
        success = rag_service.store_similar_incident_relationship(
            source_incident_id=request.source_incident_id,
            similar_incident_id=request.similar_incident_id,
            similarity_score=request.similarity_score,
            method=request.method
        )
        
        if success:
            return {
                "success": True,
                "message": "Similarity relationship stored"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to store relationship")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error storing similarity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_rag_info():
    """
    Get RAG service information
    
    Returns service status and database statistics.
    """
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG service not available")
    
    try:
        info = rag_service.get_service_info()
        return info
        
    except Exception as e:
        logger.error(f"Error getting RAG info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def rag_health_check():
    """
    Health check for RAG service
    """
    if not rag_service:
        return {
            "status": "unhealthy",
            "service": "RAG Retrieval",
            "error": "Service not initialized"
        }
    
    try:
        info = rag_service.get_service_info()
        return {
            "status": "healthy",
            "service": "RAG Retrieval",
            "embedding_model": info.get("embedding_model"),
            "database_stats": info.get("database_stats")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "RAG Retrieval",
            "error": str(e)
        }
