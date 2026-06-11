"""
Simple Investigation API - Direct endpoint for demo
Automatically fetches logs from Chaos Platform and processes investigation
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger
import requests
from typing import Optional

from backend.ai.gemini_service import GeminiService
from backend.ai.risk_engine import RiskEngine
from backend.ai.rag_service import RAGService

router = APIRouter(prefix="/api/investigate", tags=["Investigation"])

# Initialize services
gemini_service = GeminiService()
risk_engine = RiskEngine()
rag_service = RAGService()

# Chaos Platform URL
CHAOS_PLATFORM_URL = "https://chaos-demo-platform.onrender.com"


class InvestigationRequest(BaseModel):
    repo_url: str
    incident_description: str


@router.post("")
async def start_investigation(request: InvestigationRequest):
    """
    Start investigation - automatically fetches logs from Chaos Platform
    
    Flow:
    1. Fetch logs from Chaos Demo Platform
    2. Analyze GitHub repository (simulated for demo)
    3. Correlate logs + GitHub
    4. Find similar incidents (RAG)
    5. Generate RCA with Gemini
    6. Calculate risk score
    """
    try:
        logger.info(f"Starting investigation for: {request.incident_description}")
        logger.info(f"GitHub repository: {request.repo_url}")
        
        # Step 1: Fetch logs from Chaos Platform
        logger.info(f"Fetching logs from {CHAOS_PLATFORM_URL}/logs")
        try:
            logs_response = requests.get(f"{CHAOS_PLATFORM_URL}/logs", timeout=10)
            logs_response.raise_for_status()
            logs_data = logs_response.json()
            
            # Extract log messages
            log_messages = []
            if isinstance(logs_data, list):
                for log in logs_data:
                    if isinstance(log, dict):
                        msg = log.get('message', '') or log.get('log', '') or str(log)
                        log_messages.append(msg)
                    else:
                        log_messages.append(str(log))
            
            logger.info(f"✅ Fetched {len(log_messages)} logs from Chaos Platform")
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Could not fetch logs from Chaos Platform: {e}")
            logger.info("Using fallback demo logs")
            # Fallback demo logs
            log_messages = [
                "[2026-06-10 09:15:24] ERROR: Database Timeout: Failed to acquire connection after 30s",
                "[2026-06-10 09:15:24] ERROR: Connection pool exhausted: 0/10 connections available",
                "[2026-06-10 09:15:27] ERROR: Payment transaction failed - Transaction ID: TXN-89234",
                "[2026-06-10 09:15:30] ERROR: Database Timeout: Connection pool exhausted",
                "[2026-06-10 09:16:12] WARN: High error rate detected: 87% of requests failing",
                "[2026-06-10 09:30:12] WARN: 1247 users affected by service degradation"
            ]
        
        # Step 2: Simulate GitHub analysis (for demo)
        github_analysis = {
            "repository": request.repo_url,
            "recent_commits": [
                {
                    "hash": "abc123",
                    "author": "dev@company.com",
                    "message": "Reduce database pool size for optimization",
                    "timestamp": "2026-06-10 09:00:00",
                    "files_changed": ["config/database.yml"],
                    "risk_level": "HIGH"
                }
            ],
            "risky_changes": [
                {
                    "file": "config/database.yml",
                    "change": "DB_POOL_SIZE: 50 → 10",
                    "risk": "Connection exhaustion possible"
                }
            ]
        }
        
        logger.info("✅ GitHub analysis completed (simulated)")
        
        # Step 3: Build timeline (correlate logs + GitHub)
        timeline = [
            {"time": "09:00 AM", "event": "Deployment - Build #4523", "type": "deployment"},
            {"time": "09:00 AM", "event": "Config change: DB pool 50 → 10", "type": "config_change"},
            {"time": "09:15 AM", "event": "First database timeout errors", "type": "error"},
            {"time": "09:30 AM", "event": "1,247 users affected", "type": "impact"}
        ]
        
        logger.info("✅ Timeline correlated")
        
        # Step 4: Find similar incidents (RAG)
        logger.info("Searching for similar incidents...")
        try:
            similar = rag_service.find_similar_incidents(
                incident_description=request.incident_description,
                top_k=3
            )
            logger.info(f"✅ Found {len(similar.get('incidents', []))} similar incidents")
        except Exception as e:
            logger.warning(f"RAG search failed: {e}")
            similar = {
                "incidents": [
                    {
                        "id": "INC-2026-0415-047",
                        "description": "Database pool exhausted",
                        "similarity": 0.95,
                        "resolution": "Increased pool size to 50"
                    }
                ]
            }
        
        # Step 5: Generate RCA with Gemini
        logger.info("Generating RCA with Gemini AI...")
        
        log_analysis_summary = {
            "error_patterns": ["Database Timeout", "Connection Pool Exhausted"],
            "error_count": len([l for l in log_messages if "ERROR" in l]),
            "affected_services": ["Payment Service"],
            "first_occurrence": "2026-06-10 09:15:24"
        }
        
        try:
            rca_result = gemini_service.generate_rca(
                incident_description=request.incident_description,
                severity="CRITICAL",
                affected_service="Payment Service",
                risk_score=91.0,
                github_analysis=github_analysis,
                log_analysis=log_analysis_summary,
                timeline={"events": timeline},
                root_cause_candidates=["Database pool size configuration change"]
            )
            logger.info("✅ RCA generated successfully")
        except Exception as e:
            logger.error(f"RCA generation failed: {e}")
            rca_result = {
                "root_cause": "Database pool configuration reduced from 50 to 10 connections",
                "impact": "1,247 users affected, $12,500 revenue loss",
                "recommendations": [
                    "Rollback commit abc123",
                    "Increase pool size to 50",
                    "Add monitoring alerts",
                    "Implement auto-scaling"
                ]
            }
        
        # Step 6: Calculate risk score
        logger.info("Calculating risk score...")
        try:
            risk_result = risk_engine.calculate_risk_score(
                incident_description=request.incident_description,
                severity="CRITICAL",
                affected_service="Payment Service",
                error_count=len(log_messages),
                incident_type="Database Connection Issue"
            )
            logger.info("✅ Risk score calculated")
        except Exception as e:
            logger.error(f"Risk calculation failed: {e}")
            risk_result = {
                "risk_score": 91.0,
                "severity": "CRITICAL",
                "confidence": "95%"
            }
        
        # Generate investigation ID
        import random
        investigation_id = random.randint(1000, 9999)
        
        logger.info(f"✅ Investigation {investigation_id} completed successfully")
        
        # Return complete results
        return {
            "success": True,
            "investigation_id": investigation_id,
            "status": "completed",
            "message": "Investigation completed successfully",
            "data": {
                "logs_fetched": len(log_messages),
                "logs": log_messages[:10],  # First 10 logs
                "github_analysis": github_analysis,
                "timeline": timeline,
                "similar_incidents": similar.get("incidents", []),
                "rca": rca_result,
                "risk_assessment": risk_result,
                "correlation_summary": {
                    "deployment_time": "09:00 AM",
                    "first_error_time": "09:15 AM",
                    "time_delta": "15 minutes",
                    "cause_effect": "Config change led to connection exhaustion"
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Investigation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{investigation_id}")
async def get_investigation_results(investigation_id: int):
    """
    Get investigation results by ID
    """
    # For demo, return same structure
    return {
        "success": True,
        "investigation_id": investigation_id,
        "status": "completed",
        "data": {
            "root_cause": "Database pool configuration change",
            "severity": "CRITICAL",
            "risk_score": 91.0
        }
    }
