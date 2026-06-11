"""
Knowledge Base and Embedding API Routes
"""
from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import List

from backend.schemas.knowledge import (
    IncidentCreate,
    RCAReportCreate,
    KnowledgeEntryCreate,
    IncidentResponse,
    EmbeddingRequest,
    EmbeddingBatchRequest,
    EmbeddingResponse,
    SimilarityRequest,
    SimilarityResponse,
    SearchRequest,
    SearchResponse
)
from backend.ai.knowledge_base import KnowledgeBaseService
from backend.ai.embedding_service import EmbeddingService
from backend.database.connection import init_db

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge Base & Embeddings"])

# Initialize services
try:
    kb_service = KnowledgeBaseService()
    embedding_service = EmbeddingService()
    logger.info("Knowledge base and embedding services initialized")
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    kb_service = None
    embedding_service = None


@router.post("/init-db")
async def initialize_database():
    """
    Initialize database - create all tables
    
    Run this once to set up the knowledge base tables.
    """
    try:
        success = init_db()
        if success:
            return {
                "success": True,
                "message": "Database initialized successfully",
                "tables": ["incidents", "rca_reports", "knowledge_base", "similar_incidents"]
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to initialize database")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/incidents")
async def store_incident(incident: IncidentCreate):
    """
    Store a new incident in the knowledge base
    
    **Test 1 Requirement:** Insert record → Stored successfully
    
    Example:
    ```json
    {
      "incident_id": "INC-2024-001",
      "description": "Database connection timeout",
      "severity": "Critical",
      "affected_service": "payment",
      "risk_score": 85.0,
      "confidence": 90.0
    }
    ```
    """
    if not kb_service:
        raise HTTPException(status_code=503, detail="Knowledge base service not available")
    
    try:
        result = kb_service.store_incident(
            incident_id=incident.incident_id,
            description=incident.description,
            severity=incident.severity,
            affected_service=incident.affected_service,
            risk_score=incident.risk_score,
            confidence=incident.confidence,
            metadata=incident.metadata
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("message", "Failed to store incident"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error storing incident: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
async def get_incident(incident_id: str):
    """
    Retrieve incident by ID
    
    **Test 2 Requirement:** Retrieve record → Correct record returned
    
    Example: GET /api/knowledge/incidents/INC-2024-001
    """
    if not kb_service:
        raise HTTPException(status_code=503, detail="Knowledge base service not available")
    
    try:
        incident = kb_service.get_incident(incident_id)
        
        if not incident:
            raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
        
        return incident
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving incident: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/incidents")
async def list_incidents(
    limit: int = 100,
    severity: str = None,
    service: str = None
):
    """
    List all incidents with optional filters
    
    Query parameters:
    - limit: Maximum number of results (default: 100)
    - severity: Filter by severity (Low/Medium/High/Critical)
    - service: Filter by affected service
    """
    if not kb_service:
        raise HTTPException(status_code=503, detail="Knowledge base service not available")
    
    try:
        incidents = kb_service.get_all_incidents(
            limit=limit,
            severity=severity,
            service=service
        )
        
        return {
            "incidents": incidents,
            "count": len(incidents),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error listing incidents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rca-reports")
async def store_rca_report(report: RCAReportCreate):
    """
    Store RCA report for an incident
    
    Links RCA analysis to an existing incident.
    """
    if not kb_service:
        raise HTTPException(status_code=503, detail="Knowledge base service not available")
    
    try:
        result = kb_service.store_rca_report(
            incident_id=report.incident_id,
            root_cause=report.root_cause,
            impact_analysis=report.impact_analysis,
            recommendations=report.recommendations,
            prevention_measures=report.prevention_measures,
            rca_text=report.rca_text,
            model_used=report.model_used,
            root_cause_candidates=report.root_cause_candidates
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to store RCA report"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error storing RCA report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/entries")
async def store_knowledge_entry(entry: KnowledgeEntryCreate):
    """
    Store knowledge base entry
    
    Entry types:
    - incident_description: Incident description
    - root_cause: Root cause analysis
    - fix: Fix/solution applied
    - recommendation: Recommendation for prevention
    """
    if not kb_service:
        raise HTTPException(status_code=503, detail="Knowledge base service not available")
    
    try:
        result = kb_service.store_knowledge_entry(
            incident_id=entry.incident_id,
            entry_type=entry.entry_type,
            title=entry.title,
            content=entry.content,
            tags=entry.tags
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to store entry"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error storing knowledge entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResponse)
async def search_knowledge_base(request: SearchRequest):
    """
    Search knowledge base
    
    Searches through stored knowledge entries.
    Will be enhanced with semantic search using embeddings.
    """
    if not kb_service:
        raise HTTPException(status_code=503, detail="Knowledge base service not available")
    
    try:
        results = kb_service.search_knowledge_base(
            query=request.query,
            entry_type=request.entry_type,
            limit=request.limit
        )
        
        return {
            "results": results,
            "count": len(results),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embeddings/generate", response_model=EmbeddingResponse)
async def generate_embedding(request: EmbeddingRequest):
    """
    Generate embedding for text
    
    **Test 1 Requirement:** Generate embedding → Vector created
    
    Converts text into a vector representation for similarity search.
    
    Example:
    ```json
    {
      "text": "Database connection timeout causing payment failures"
    }
    ```
    """
    if not embedding_service:
        raise HTTPException(status_code=503, detail="Embedding service not available")
    
    try:
        embedding = embedding_service.generate_embedding(request.text)
        
        return {
            "embedding": embedding,
            "dimensions": len(embedding),
            "model": embedding_service.model_name,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embeddings/batch")
async def generate_embeddings_batch(request: EmbeddingBatchRequest):
    """
    Generate embeddings for multiple texts
    
    **Test 2 Requirement:** Store embedding → Saved successfully
    
    Batch processing for efficiency.
    """
    if not embedding_service:
        raise HTTPException(status_code=503, detail="Embedding service not available")
    
    try:
        embeddings = embedding_service.generate_embeddings_batch(request.texts)
        
        return {
            "embeddings": embeddings,
            "count": len(embeddings),
            "dimensions": len(embeddings[0]) if embeddings else 0,
            "model": embedding_service.model_name,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error generating batch embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embeddings/similarity", response_model=SimilarityResponse)
async def calculate_similarity(request: SimilarityRequest):
    """
    Calculate similarity between two embeddings
    
    Returns cosine similarity score (0.0 to 1.0)
    - 1.0 = identical
    - 0.0 = completely different
    """
    if not embedding_service:
        raise HTTPException(status_code=503, detail="Embedding service not available")
    
    try:
        similarity = embedding_service.calculate_similarity(
            request.embedding1,
            request.embedding2
        )
        
        return {
            "similarity": similarity,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/embeddings/info")
async def get_embedding_info():
    """
    Get embedding service information
    
    Returns details about the embedding model.
    """
    if not embedding_service:
        raise HTTPException(status_code=503, detail="Embedding service not available")
    
    try:
        info = embedding_service.get_embedding_info()
        return {
            **info,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error getting embedding info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/store-incident-with-embedding")
async def store_incident_with_embedding(
    incident: IncidentCreate,
    generate_embeddings: bool = True
):
    """
    Store incident and generate embeddings in one call
    
    Complete workflow:
    1. Store incident
    2. Generate embeddings
    3. Store knowledge entries with embeddings
    """
    if not kb_service or not embedding_service:
        raise HTTPException(status_code=503, detail="Services not available")
    
    try:
        # Store incident
        incident_result = kb_service.store_incident(
            incident_id=incident.incident_id,
            description=incident.description,
            severity=incident.severity,
            affected_service=incident.affected_service,
            risk_score=incident.risk_score,
            confidence=incident.confidence,
            metadata=incident.metadata
        )
        
        if not incident_result["success"]:
            raise HTTPException(status_code=400, detail="Failed to store incident")
        
        # Generate embeddings if requested
        embeddings = {}
        if generate_embeddings:
            embedding = embedding_service.generate_embedding(incident.description)
            embeddings["incident_description"] = embedding
            
            # Store knowledge entry with embedding
            kb_service.store_knowledge_entry(
                incident_id=incident.incident_id,
                entry_type="incident_description",
                title=f"Incident: {incident.incident_id}",
                content=incident.description,
                embedding=embedding,
                embedding_model=embedding_service.model_name
            )
        
        return {
            "success": True,
            "incident_id": incident.incident_id,
            "embeddings_generated": len(embeddings) > 0,
            "embedding_dimensions": len(embeddings["incident_description"]) if embeddings else 0
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in complete workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))
