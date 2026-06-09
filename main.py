from fastapi import FastAPI
from pydantic import BaseModel

from agents.log_agent import get_logs
from agents.github_agent import get_github_analysis
from agents.timeline_agent import get_timeline
from agents.investigation_agent import investigate_incident
from database import engine, SessionLocal
from models import Base, Investigation
from agents.classification_agent import classify_incident
from agents.investigation_engine import generate_investigation

Base.metadata.create_all(bind=engine)
app = FastAPI()

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

    db = SessionLocal()

    incident = Investigation(
        repo_url=data.repo_url,
        incident_description=data.incident_description,
        status="started",
        severity="Pending",
        root_cause="Pending"
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    db.close()

    return {
        "investigation_id": incident.id,
        "repo_url": incident.repo_url,
        "status": incident.status
    }

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
    return {
        "logs": get_logs()
    }

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

    return generate_investigation(
        "Users unable to complete payments",
        github_data
    )

@app.get("/investigations/{investigation_id}")
def get_investigation(investigation_id: int):

    db = SessionLocal()

    incident = db.query(
        Investigation
    ).filter(
        Investigation.id == investigation_id
    ).first()

    db.close()

    if not incident:
        return {
            "error": "Investigation not found"
        }

    return {
        "id": incident.id,
        "repo_url": incident.repo_url,
        "incident_description": incident.incident_description,
        "status": incident.status,
        "severity": incident.severity,
        "root_cause": incident.root_cause
    }

@app.get("/timeline/{investigation_id}")
def get_timeline_by_id(
    investigation_id: int
):

    db = SessionLocal()

    incident = db.query(
        Investigation
    ).filter(
        Investigation.id == investigation_id
    ).first()

    db.close()

    if not incident:
        return {
            "error": "Investigation not found"
        }

    return {
        "investigation_id": incident.id,
        "timeline": [
            "Investigation Started",
            "Incident Received",
            "Classification Complete"
        ]
    }