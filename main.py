from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
from loguru import logger
import sys

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO"
)

# Load environment variables
load_dotenv()

from agents.log_agent import get_logs, get_failures, get_status
from agents.github_agent import get_github_analysis
from agents.timeline_agent import get_timeline
from agents.investigation_agent import investigate_incident
from database import engine, SessionLocal
from models import Base, Investigation
from agents.classification_agent import classify_incident
from agents.investigation_engine import generate_investigation

Base.metadata.create_all(bind=engine)
app = FastAPI(title="SmartOps Investigation Backend", version="1.0.0")

# Member 3 (AI/RCA Engine) Configuration
MEMBER3_URL = os.environ.get("MEMBER3_API_URL", "http://localhost:8002/api").rstrip("/api")

# CORS Configuration
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InvestigationRequest(BaseModel):
    repo_url: str
    incident_description: str
@app.get("/")
def home():
    return {"message": "SmartOps Backend Running"}

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
@app.post("/investigate")
def investigate(data: InvestigationRequest):
    """
    Full investigation endpoint that processes GitHub + Logs + Analysis.
    This is the main endpoint that orchestrates all agents.
    """
    db = SessionLocal()

    # 1. Create investigation record
    incident = Investigation(
        repo_url=data.repo_url,
        incident_description=data.incident_description,
        status="investigating",
        severity="Pending",
        root_cause="Pending"
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    try:
        # 2. Run GitHub analysis
        github_data = get_github_analysis(data.repo_url, limit=20)
        
        # 3. Fetch logs
        log_data = get_logs(level="ERROR", limit=100)
        
        # 4. Generate investigation
        investigation_result = generate_investigation(
            data.incident_description,
            github_data,
            log_data
        )
        
        # 5. Generate AI-powered RCA via Member 3
        ai_rca = None
        try:
            rca_response = requests.post(
                f"{MEMBER3_URL}/api/generate-rca",
                json={
                    "incident": data.incident_description,
                    "logs": f"{log_data.get('error_count', 0)} errors detected from {log_data.get('source', 'unknown')}",
                    "timeline": investigation_result.get("timeline_summary", "Events analyzed"),
                    "severity": investigation_result.get("severity", "medium").lower(),
                    "affected_service": "investigation",
                    "risk_score": investigation_result.get("risk_score", 50.0),
                    "github_analysis": github_data,
                    "log_analysis": log_data,
                    "timeline_data": {"events": investigation_result.get("timeline", [])},
                    "root_cause_candidates": [investigation_result.get("probable_root_cause", {})]
                },
                timeout=30
            )
            
            if rca_response.status_code == 200:
                ai_rca = rca_response.json()
                logger.info("✅ AI-powered RCA generated successfully via Member 3")
            else:
                logger.warning(f"⚠️ Member 3 RCA generation failed: {rca_response.status_code}")
        except requests.exceptions.ConnectionError:
            logger.warning("⚠️ Member 3 (AI/RCA Engine) not available - continuing without AI RCA")
        except requests.exceptions.Timeout:
            logger.warning("⚠️ Member 3 RCA generation timed out")
        except Exception as e:
            logger.warning(f"⚠️ Failed to connect to Member 3: {str(e)}")
        
        # 6. Update database with results
        incident.status = "completed"
        incident.severity = investigation_result.get("severity", "Unknown")
        incident.root_cause = investigation_result.get("probable_root_cause", {}).get("description", "Unknown")
        db.commit()
        db.refresh(incident)
        
        # 7. Return complete results with AI RCA
        response_data = {
            "investigation_id": incident.id,
            "status": "completed",
            "repo_url": incident.repo_url,
            "incident_description": incident.incident_description,
            "investigation": investigation_result,
            "github_analysis": {
                "success": github_data.get("success", False),
                "total_commits": github_data.get("total_commits_analyzed", 0),
                "config_changes": len(github_data.get("config_changes", []))
            },
            "log_analysis": {
                "source": log_data.get("source", "unknown"),
                "total_logs": log_data.get("total_logs", 0),
                "error_count": log_data.get("error_count", 0)
            }
        }
        
        # Add AI RCA if available
        if ai_rca and ai_rca.get("success"):
            response_data["ai_rca"] = {
                "rca_text": ai_rca.get("rca_text", ""),
                "model_used": ai_rca.get("model_used", "gemini-flash-latest"),
                "generated_by": "Member 3 - AI/RCA Engine"
            }
            logger.info("✅ Complete investigation with AI-powered RCA")
        else:
            logger.info("✅ Investigation complete (without AI RCA)")
        
        return response_data
    
    except Exception as e:
        # Handle errors gracefully
        incident.status = "failed"
        incident.root_cause = f"Investigation failed: {str(e)}"
        db.commit()
        
        return {
            "investigation_id": incident.id,
            "status": "failed",
            "error": str(e)
        }
    
    finally:
        db.close()

@app.get("/investigations")
def get_investigations():

    db = SessionLocal()

    investigations = db.query(Investigation).all()

    result = []

    for i in investigations:
        result.append({
        "id": i.id,
        "repo_url": i.repo_url,
        "incident_description": i.incident_description,
        "status": i.status
    })

    db.close()

    return result

@app.get("/logs")
def logs():
    """Fetch logs from Project 2 or fallback data"""
    log_data = get_logs(level="ERROR", limit=100)
    return log_data

@app.get("/timeline")
def timeline():
    return {
        "timeline": get_timeline()
    }


@app.get("/status")
def status():
    return investigate_incident()

@app.get("/github-test")
def github_test():

    return get_github_analysis(
        "https://github.com/psf/requests"
    )

@app.get("/classify-test")
def classify_test():

    return classify_incident(
        "Users unable to complete payments"
    )

@app.get("/engine-test")
def engine_test():

    github_data = get_github_analysis(
        "https://github.com/psf/requests"
    )
    
    log_data = get_logs(level="ERROR", limit=50)

    return generate_investigation(
        "Users unable to complete payments",
        github_data,
        log_data
    )


@app.get("/failures")
def failures():
    """Get failure events from Project 2"""
    return get_failures()


@app.get("/project2-status")
def project2_status():
    """Check Project 2 (Chaos Demo) status"""
    return get_status()

@app.get("/investigations/{investigation_id}")
def get_investigation(investigation_id: int):
    """Get complete investigation results including timeline and analysis"""
    db = SessionLocal()

    incident = db.query(
        Investigation
    ).filter(
        Investigation.id == investigation_id
    ).first()

    if not incident:
        db.close()
        return {
            "error": "Investigation not found"
        }
    
    # If investigation was completed, regenerate the analysis for display
    investigation_data = None
    if incident.status == "completed" and incident.repo_url:
        try:
            github_data = get_github_analysis(incident.repo_url, limit=20)
            log_data = get_logs(level="ERROR", limit=100)
            investigation_data = generate_investigation(
                incident.incident_description,
                github_data,
                log_data
            )
        except:
            investigation_data = None

    db.close()

    result = {
        "id": incident.id,
        "repo_url": incident.repo_url,
        "incident_description": incident.incident_description,
        "status": incident.status,
        "severity": incident.severity,
        "root_cause": incident.root_cause
    }
    
    # Add full investigation data if available
    if investigation_data:
        result["investigation"] = investigation_data
    
    return result

@app.get("/timeline/{investigation_id}")
def get_timeline_by_id(investigation_id: int):
    """Get investigation timeline with all events"""
    db = SessionLocal()

    incident = db.query(
        Investigation
    ).filter(
        Investigation.id == investigation_id
    ).first()

    if not incident:
        db.close()
        return {
            "error": "Investigation not found"
        }
    
    # Generate timeline from investigation
    timeline = [
        {
            "time": "Start",
            "event": "Investigation Started",
            "type": "system"
        },
        {
            "time": "Step 1",
            "event": f"Incident Received: {incident.incident_description}",
            "type": "incident"
        }
    ]
    
    # If completed, add actual timeline
    if incident.status == "completed" and incident.repo_url:
        try:
            github_data = get_github_analysis(incident.repo_url, limit=10)
            log_data = get_logs(level="ERROR", limit=50)
            investigation_data = generate_investigation(
                incident.incident_description,
                github_data,
                log_data
            )
            
            # Use the generated timeline
            if investigation_data.get("timeline"):
                timeline = investigation_data["timeline"]
        except:
            pass
    
    timeline.append({
        "time": "Final",
        "event": f"Investigation {incident.status.upper()}",
        "type": "system"
    })

    db.close()

    return {
        "investigation_id": incident.id,
        "status": incident.status,
        "severity": incident.severity,
        "timeline": timeline
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
