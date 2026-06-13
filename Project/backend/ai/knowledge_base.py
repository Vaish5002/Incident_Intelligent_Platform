"""
Knowledge Base Service
Manages storage and retrieval of historical incidents
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session

from database.models import Incident, RCAReport, KnowledgeBase, SimilarIncident
from database.connection import get_db_session


class KnowledgeBaseService:
    """
    Service for managing the knowledge base of historical incidents
    """
    
    def __init__(self):
        """Initialize knowledge base service"""
        logger.info("Knowledge base service initialized")
    
    def store_incident(
        self,
        incident_id: str,
        description: str,
        severity: str,
        affected_service: str,
        risk_score: float,
        confidence: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store a new incident in the knowledge base
        
        Args:
            incident_id: Unique incident identifier
            description: Incident description
            severity: Severity level (Low/Medium/High/Critical)
            affected_service: Service affected
            risk_score: Risk score (0-100)
            confidence: Confidence level (0-100)
            metadata: Additional metadata
            
        Returns:
            Dictionary with stored incident info
        """
        try:
            db = get_db_session()
            
            # Check if incident already exists
            existing = db.query(Incident).filter(Incident.incident_id == incident_id).first()
            if existing:
                logger.warning(f"Incident {incident_id} already exists")
                return {
                    "success": False,
                    "message": "Incident already exists",
                    "incident_id": incident_id
                }
            
            # Create new incident
            incident = Incident(
                incident_id=incident_id,
                description=description,
                severity=severity,
                affected_service=affected_service,
                risk_score=risk_score,
                confidence=confidence,
                status="open",
                metadata_json=metadata or {}
            )
            
            db.add(incident)
            db.commit()
            db.refresh(incident)
            
            logger.info(f"Incident {incident_id} stored successfully")
            
            return {
                "success": True,
                "incident_id": incident_id,
                "id": incident.id,
                "created_at": incident.created_at.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error storing incident: {e}")
            if 'db' in locals():
                db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            if 'db' in locals():
                db.close()
    
    def store_rca_report(
        self,
        incident_id: str,
        root_cause: str,
        impact_analysis: str,
        recommendations: str,
        prevention_measures: str,
        rca_text: str,
        model_used: str,
        root_cause_candidates: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Store RCA report for an incident
        
        Args:
            incident_id: Incident identifier
            root_cause: Root cause analysis
            impact_analysis: Impact assessment
            recommendations: Recommendations
            prevention_measures: Prevention measures
            rca_text: Full RCA text (markdown)
            model_used: AI model used
            root_cause_candidates: List of root cause candidates
            
        Returns:
            Dictionary with success status
        """
        try:
            db = get_db_session()
            
            # Find incident
            incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
            if not incident:
                return {
                    "success": False,
                    "error": f"Incident {incident_id} not found"
                }
            
            # Check if RCA already exists
            existing_rca = db.query(RCAReport).filter(RCAReport.incident_id == incident.id).first()
            if existing_rca:
                # Update existing
                existing_rca.root_cause = root_cause
                existing_rca.impact_analysis = impact_analysis
                existing_rca.recommendations = recommendations
                existing_rca.prevention_measures = prevention_measures
                existing_rca.rca_text = rca_text
                existing_rca.model_used = model_used
                existing_rca.root_cause_candidates = root_cause_candidates
                existing_rca.generated_at = datetime.utcnow()
            else:
                # Create new
                rca_report = RCAReport(
                    incident_id=incident.id,
                    root_cause=root_cause,
                    impact_analysis=impact_analysis,
                    recommendations=recommendations,
                    prevention_measures=prevention_measures,
                    rca_text=rca_text,
                    model_used=model_used,
                    root_cause_candidates=root_cause_candidates
                )
                db.add(rca_report)
            
            # Update incident status
            incident.status = "resolved"
            incident.resolved_at = datetime.utcnow()
            
            db.commit()
            
            logger.info(f"RCA report stored for incident {incident_id}")
            
            return {
                "success": True,
                "incident_id": incident_id
            }
            
        except Exception as e:
            logger.error(f"Error storing RCA report: {e}")
            if 'db' in locals():
                db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            if 'db' in locals():
                db.close()
    
    def store_knowledge_entry(
        self,
        incident_id: str,
        entry_type: str,
        title: str,
        content: str,
        embedding: Optional[List[float]] = None,
        embedding_model: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Store a knowledge base entry
        
        Args:
            incident_id: Incident identifier
            entry_type: Type of entry (incident_description, root_cause, fix, recommendation)
            title: Entry title
            content: Entry content
            embedding: Vector embedding
            embedding_model: Model used for embedding
            tags: Tags for categorization
            
        Returns:
            Dictionary with success status
        """
        try:
            db = get_db_session()
            
            # Find incident
            incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
            if not incident:
                return {
                    "success": False,
                    "error": f"Incident {incident_id} not found"
                }
            
            # Create knowledge entry
            entry = KnowledgeBase(
                incident_id=incident.id,
                entry_type=entry_type,
                title=title,
                content=content,
                embedding=embedding,
                embedding_model=embedding_model,
                tags=tags or []
            )
            
            db.add(entry)
            db.commit()
            db.refresh(entry)
            
            logger.info(f"Knowledge entry stored: {entry_type} for {incident_id}")
            
            return {
                "success": True,
                "entry_id": entry.id,
                "incident_id": incident_id
            }
            
        except Exception as e:
            logger.error(f"Error storing knowledge entry: {e}")
            if 'db' in locals():
                db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            if 'db' in locals():
                db.close()
    
    def get_incident(self, incident_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve incident by ID
        
        Args:
            incident_id: Incident identifier
            
        Returns:
            Dictionary with incident data or None
        """
        try:
            db = get_db_session()
            
            incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
            if not incident:
                return None
            
            # Get RCA report if exists
            rca = db.query(RCAReport).filter(RCAReport.incident_id == incident.id).first()
            
            return {
                "incident_id": incident.incident_id,
                "description": incident.description,
                "severity": incident.severity,
                "affected_service": incident.affected_service,
                "status": incident.status,
                "risk_score": incident.risk_score,
                "confidence": incident.confidence,
                "occurred_at": incident.occurred_at.isoformat() if incident.occurred_at else None,
                "resolved_at": incident.resolved_at.isoformat() if incident.resolved_at else None,
                "metadata": incident.metadata_json,
                "rca_report": {
                    "root_cause": rca.root_cause,
                    "recommendations": rca.recommendations,
                    "prevention_measures": rca.prevention_measures,
                    "rca_text": rca.rca_text
                } if rca else None
            }
            
        except Exception as e:
            logger.error(f"Error retrieving incident: {e}")
            return None
        finally:
            if 'db' in locals():
                db.close()
    
    def get_all_incidents(
        self,
        limit: int = 100,
        severity: Optional[str] = None,
        service: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all incidents with optional filters
        
        Args:
            limit: Maximum number of incidents to return
            severity: Filter by severity
            service: Filter by affected service
            
        Returns:
            List of incident dictionaries
        """
        try:
            db = get_db_session()
            
            query = db.query(Incident)
            
            if severity:
                query = query.filter(Incident.severity == severity)
            if service:
                query = query.filter(Incident.affected_service == service)
            
            incidents = query.order_by(Incident.occurred_at.desc()).limit(limit).all()
            
            return [
                {
                    "incident_id": inc.incident_id,
                    "description": inc.description,
                    "severity": inc.severity,
                    "affected_service": inc.affected_service,
                    "status": inc.status,
                    "risk_score": inc.risk_score,
                    "occurred_at": inc.occurred_at.isoformat() if inc.occurred_at else None
                }
                for inc in incidents
            ]
            
        except Exception as e:
            logger.error(f"Error retrieving incidents: {e}")
            return []
        finally:
            if 'db' in locals():
                db.close()
    
    def search_knowledge_base(
        self,
        query: str,
        entry_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search knowledge base entries
        
        Args:
            query: Search query
            entry_type: Filter by entry type
            limit: Maximum results
            
        Returns:
            List of matching entries
        """
        try:
            db = get_db_session()
            
            # Simple text search for now (will be enhanced with embeddings)
            query_filter = KnowledgeBase.content.contains(query)
            
            if entry_type:
                query_filter = query_filter & (KnowledgeBase.entry_type == entry_type)
            
            entries = db.query(KnowledgeBase)\
                .filter(query_filter)\
                .order_by(KnowledgeBase.times_retrieved.desc())\
                .limit(limit)\
                .all()
            
            # Increment retrieval count
            for entry in entries:
                entry.times_retrieved += 1
            db.commit()
            
            return [
                {
                    "entry_id": entry.id,
                    "incident_id": entry.incident.incident_id,
                    "entry_type": entry.entry_type,
                    "title": entry.title,
                    "content": entry.content,
                    "tags": entry.tags
                }
                for entry in entries
            ]
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
        finally:
            if 'db' in locals():
                db.close()
