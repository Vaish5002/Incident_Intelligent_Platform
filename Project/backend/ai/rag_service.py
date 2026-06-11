"""
RAG Retrieval Service
Finds similar historical incidents using embeddings
"""
from typing import List, Dict, Any, Optional
from loguru import logger
from sqlalchemy.orm import Session

from backend.ai.embedding_service import EmbeddingService
from backend.ai.knowledge_base import KnowledgeBaseService
from backend.database.connection import get_db_session
from backend.database.models import Incident, KnowledgeBase, SimilarIncident


class RAGService:
    """
    Retrieval-Augmented Generation Service
    
    Finds similar historical incidents using semantic search
    and provides context for AI-powered RCA generation.
    """
    
    def __init__(self):
        """Initialize RAG service"""
        self.embedding_service = EmbeddingService()
        self.kb_service = KnowledgeBaseService()
        logger.info("RAG service initialized")
    
    def find_similar_incidents(
        self,
        incident_description: str,
        logs: Optional[str] = None,
        top_k: int = 5,
        similarity_threshold: float = 0.3
    ) -> Dict[str, Any]:
        """
        Find similar historical incidents
        
        Flow:
        New Incident → Embedding → Similarity Search → Top Matches
        
        Args:
            incident_description: Current incident description
            logs: Optional log data
            top_k: Number of top matches to return
            similarity_threshold: Minimum similarity score (0.0 to 1.0)
            
        Returns:
            Dictionary with similar incidents and match metadata
        """
        try:
            # Step 1: Generate embedding for new incident
            query_text = incident_description
            if logs:
                query_text = f"{incident_description} {logs}"
            
            logger.info(f"Generating embedding for query: {incident_description[:100]}...")
            query_embedding = self.embedding_service.generate_embedding(query_text)
            
            if not query_embedding or all(v == 0 for v in query_embedding):
                logger.warning("Failed to generate valid embedding")
                return {
                    "success": False,
                    "message": "Failed to generate embedding",
                    "similar_incidents": [],
                    "count": 0
                }
            
            # Step 2: Get all knowledge base entries with embeddings
            db = get_db_session()
            
            knowledge_entries = db.query(KnowledgeBase)\
                .filter(KnowledgeBase.embedding.isnot(None))\
                .all()
            
            if not knowledge_entries:
                logger.info("No historical incidents in database")
                db.close()
                return {
                    "success": True,
                    "message": "No historical incidents found",
                    "similar_incidents": [],
                    "count": 0
                }
            
            logger.info(f"Searching through {len(knowledge_entries)} knowledge entries")
            
            # Step 3: Calculate similarities
            similarities = []
            for entry in knowledge_entries:
                if not entry.embedding:
                    continue
                
                similarity = self.embedding_service.calculate_similarity(
                    query_embedding,
                    entry.embedding
                )
                
                if similarity >= similarity_threshold:
                    similarities.append({
                        "entry": entry,
                        "similarity": similarity
                    })
            
            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            
            # Take top K
            top_matches = similarities[:top_k]
            
            # Step 4: Build response with incident details
            similar_incidents = []
            for match in top_matches:
                entry = match["entry"]
                incident = db.query(Incident).filter(Incident.id == entry.incident_id).first()
                
                if incident:
                    # Get RCA if available
                    rca_report = None
                    if incident.rca_report:
                        rca_report = {
                            "root_cause": incident.rca_report.root_cause,
                            "recommendations": incident.rca_report.recommendations,
                            "prevention_measures": incident.rca_report.prevention_measures
                        }
                    
                    similar_incidents.append({
                        "incident_id": incident.incident_id,
                        "description": incident.description,
                        "severity": incident.severity,
                        "affected_service": incident.affected_service,
                        "risk_score": incident.risk_score,
                        "status": incident.status,
                        "similarity": round(match["similarity"] * 100, 2),  # Convert to percentage
                        "similarity_raw": match["similarity"],
                        "occurred_at": incident.occurred_at.isoformat() if incident.occurred_at else None,
                        "rca_summary": rca_report
                    })
            
            db.close()
            
            if similar_incidents:
                logger.info(f"Found {len(similar_incidents)} similar incidents (top match: {similar_incidents[0]['similarity']}%)")
            else:
                logger.info("No similar incidents found above threshold")
            
            return {
                "success": True,
                "message": f"Found {len(similar_incidents)} similar incidents",
                "similar_incidents": similar_incidents,
                "count": len(similar_incidents),
                "top_similarity": similar_incidents[0]["similarity"] if similar_incidents else 0
            }
            
        except Exception as e:
            logger.error(f"Error finding similar incidents: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "similar_incidents": [],
                "count": 0
            }
    
    def store_similar_incident_relationship(
        self,
        source_incident_id: str,
        similar_incident_id: str,
        similarity_score: float,
        method: str = "embedding"
    ) -> bool:
        """
        Store a similar incident relationship
        
        Args:
            source_incident_id: Source incident ID
            similar_incident_id: Similar incident ID
            similarity_score: Similarity score (0.0 to 1.0)
            method: Method used to find similarity
            
        Returns:
            Success status
        """
        try:
            db = get_db_session()
            
            # Get incident IDs
            source = db.query(Incident).filter(Incident.incident_id == source_incident_id).first()
            similar = db.query(Incident).filter(Incident.incident_id == similar_incident_id).first()
            
            if not source or not similar:
                logger.warning(f"Incidents not found: {source_incident_id}, {similar_incident_id}")
                db.close()
                return False
            
            # Check if relationship already exists
            existing = db.query(SimilarIncident)\
                .filter(
                    SimilarIncident.source_incident_id == source.id,
                    SimilarIncident.similar_incident_id == similar.id
                )\
                .first()
            
            if existing:
                # Update similarity score
                existing.similarity_score = similarity_score
                existing.similarity_method = method
            else:
                # Create new relationship
                relationship = SimilarIncident(
                    source_incident_id=source.id,
                    similar_incident_id=similar.id,
                    similarity_score=similarity_score,
                    similarity_method=method
                )
                db.add(relationship)
            
            db.commit()
            db.close()
            
            logger.info(f"Stored similarity relationship: {source_incident_id} <-> {similar_incident_id} ({similarity_score:.2f})")
            return True
            
        except Exception as e:
            logger.error(f"Error storing similar incident relationship: {e}")
            if 'db' in locals():
                db.rollback()
                db.close()
            return False
    
    def get_rag_context(
        self,
        incident_description: str,
        logs: Optional[str] = None,
        top_k: int = 3
    ) -> str:
        """
        Get RAG context for AI generation
        
        Returns formatted context from similar incidents
        for use in prompts.
        
        Args:
            incident_description: Current incident
            logs: Optional logs
            top_k: Number of similar incidents to include
            
        Returns:
            Formatted context string
        """
        result = self.find_similar_incidents(
            incident_description=incident_description,
            logs=logs,
            top_k=top_k
        )
        
        if not result["success"] or not result["similar_incidents"]:
            return "No similar historical incidents found."
        
        context_parts = ["## Similar Historical Incidents\n"]
        
        for i, incident in enumerate(result["similar_incidents"], 1):
            context_parts.append(f"\n### Similar Incident {i} ({incident['similarity']}% match)")
            context_parts.append(f"**Incident ID:** {incident['incident_id']}")
            context_parts.append(f"**Description:** {incident['description']}")
            context_parts.append(f"**Severity:** {incident['severity']}")
            context_parts.append(f"**Service:** {incident['affected_service']}")
            
            if incident.get("rca_summary"):
                rca = incident["rca_summary"]
                context_parts.append(f"\n**Past Root Cause:** {rca.get('root_cause', 'N/A')[:200]}...")
                if rca.get("recommendations"):
                    context_parts.append(f"**Past Recommendations:** {rca.get('recommendations', 'N/A')[:200]}...")
            
            context_parts.append("\n---")
        
        return "\n".join(context_parts)
    
    def retrieve_and_augment(
        self,
        incident_description: str,
        logs: Optional[str] = None,
        github_data: Optional[Dict] = None,
        timeline: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete RAG workflow: Retrieve similar incidents and augment prompt
        
        This is the main RAG method that combines retrieval with context augmentation.
        
        Args:
            incident_description: Current incident description
            logs: Log data
            github_data: GitHub analysis
            timeline: Timeline of events
            
        Returns:
            Dictionary with similar incidents and augmented context
        """
        # Find similar incidents
        similar = self.find_similar_incidents(
            incident_description=incident_description,
            logs=logs,
            top_k=5
        )
        
        # Get formatted context
        rag_context = self.get_rag_context(
            incident_description=incident_description,
            logs=logs,
            top_k=3
        )
        
        # Build augmented prompt data
        augmented_data = {
            "incident": incident_description,
            "logs": logs or "",
            "timeline": timeline or "",
            "github_data": github_data or {},
            "rag_context": rag_context,
            "similar_incidents_found": similar["count"],
            "top_similarity": similar.get("top_similarity", 0)
        }
        
        return {
            "success": True,
            "similar_incidents": similar["similar_incidents"],
            "count": similar["count"],
            "augmented_data": augmented_data,
            "rag_context": rag_context
        }
    
    def get_service_info(self) -> Dict[str, Any]:
        """
        Get RAG service information
        
        Returns:
            Service metadata
        """
        try:
            db = get_db_session()
            
            incident_count = db.query(Incident).count()
            knowledge_count = db.query(KnowledgeBase).count()
            embedding_count = db.query(KnowledgeBase)\
                .filter(KnowledgeBase.embedding.isnot(None))\
                .count()
            
            db.close()
            
            return {
                "service": "RAG Retrieval",
                "status": "operational",
                "embedding_model": self.embedding_service.model_name,
                "database_stats": {
                    "total_incidents": incident_count,
                    "knowledge_entries": knowledge_count,
                    "entries_with_embeddings": embedding_count
                },
                "capabilities": [
                    "Semantic similarity search",
                    "Historical incident retrieval",
                    "Context augmentation for AI",
                    "Similar incident tracking"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting service info: {e}")
            return {
                "service": "RAG Retrieval",
                "status": "error",
                "error": str(e)
            }
