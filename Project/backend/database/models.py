"""
Database Models for Knowledge Base
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Incident(Base):
    """
    Incident records - stores all historical incidents
    """
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Core incident data
    description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False)  # Low/Medium/High/Critical
    affected_service = Column(String(100))
    status = Column(String(20), default="open")  # open/investigating/resolved/closed
    
    # Risk assessment
    risk_score = Column(Float)
    confidence = Column(Float)
    
    # Timeline
    occurred_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadata
    metadata_json = Column(JSON)  # Additional data (logs, GitHub info, etc.)
    
    # Relationships
    rca_report = relationship("RCAReport", back_populates="incident", uselist=False)
    knowledge_entries = relationship("KnowledgeBase", back_populates="incident")
    
    def __repr__(self):
        return f"<Incident {self.incident_id}: {self.description[:50]}>"


class RCAReport(Base):
    """
    RCA Reports - stores generated root cause analysis
    """
    __tablename__ = "rca_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), unique=True, nullable=False)
    
    # RCA content
    root_cause = Column(Text, nullable=False)
    impact_analysis = Column(Text)
    recommendations = Column(Text)
    prevention_measures = Column(Text)
    
    # Full RCA text (markdown)
    rca_text = Column(Text)
    
    # AI metadata
    model_used = Column(String(50))
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Root cause candidates
    root_cause_candidates = Column(JSON)  # List of identified causes with confidence
    
    # Relationships
    incident = relationship("Incident", back_populates="rca_report")
    
    def __repr__(self):
        return f"<RCAReport for Incident {self.incident_id}>"


class KnowledgeBase(Base):
    """
    Knowledge Base - stores searchable knowledge entries with embeddings
    """
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    
    # Entry metadata
    entry_type = Column(String(50))  # incident_description, root_cause, fix, recommendation
    title = Column(String(200))
    content = Column(Text, nullable=False)
    
    # Embedding for similarity search
    embedding = Column(JSON)  # Vector representation as JSON array
    embedding_model = Column(String(50))  # Model used to generate embedding
    
    # Tags for categorization
    tags = Column(JSON)  # List of tags
    
    # Effectiveness tracking
    times_retrieved = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    incident = relationship("Incident", back_populates="knowledge_entries")
    
    def __repr__(self):
        return f"<KnowledgeEntry {self.entry_type}: {self.title}>"


class SimilarIncident(Base):
    """
    Tracks similar incident relationships
    """
    __tablename__ = "similar_incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    source_incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    similar_incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    
    similarity_score = Column(Float, nullable=False)  # 0.0 to 1.0
    similarity_method = Column(String(50))  # embedding, keyword, timeline, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Similar: {self.source_incident_id} -> {self.similar_incident_id} ({self.similarity_score:.2f})>"
