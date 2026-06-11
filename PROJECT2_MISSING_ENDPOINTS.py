"""
Missing Endpoints for Project 2 - Chaos Demo Platform
Member 2 should add these to complete the requirements
"""

# ============================================================================
# File: backend/routes/logs.py (UPDATE - Add these endpoints)
# ============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import RuntimeLog, FailureEvent, ActiveFailure

router = APIRouter()

@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    """Existing endpoint - already implemented"""
    logs = db.query(RuntimeLog).all()
    return logs


# 🆕 ADD THIS ENDPOINT
@router.get("/failures")
def get_failures(db: Session = Depends(get_db)):
    """
    Get all failure events
    Member 1 calls this endpoint!
    """
    failures = db.query(FailureEvent).order_by(
        FailureEvent.created_at.desc()
    ).limit(100).all()
    
    return failures


# 🆕 ADD THIS ENDPOINT
@router.get("/status")
def get_status(db: Session = Depends(get_db)):
    """
    Get current system status and active failures
    Member 1 calls this endpoint!
    """
    active_failures = db.query(ActiveFailure).filter(
        ActiveFailure.status == "ACTIVE"
    ).all()
    
    recent_errors = db.query(RuntimeLog).filter(
        RuntimeLog.level == "ERROR"
    ).order_by(RuntimeLog.timestamp.desc()).limit(10).all()
    
    return {
        "status": "running",
        "active_failures_count": len(active_failures),
        "active_failures": [
            {
                "id": f.id,
                "type": f.failure_type,
                "status": f.status
            } for f in active_failures
        ],
        "recent_error_count": len(recent_errors),
        "health": "ok" if len(active_failures) == 0 else "degraded"
    }


# ============================================================================
# File: backend/routes/inject_env.py (NEW FILE)
# ============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from services.log_service import create_log

router = APIRouter(prefix="/inject")


@router.post("/missing-env")
def missing_env(db: Session = Depends(get_db)):
    """
    Simulate missing environment variable failures
    Module 7 requirement
    """
    # Generate multiple error logs
    create_log(
        db,
        "ERROR",
        "Environment Variable 'DATABASE_URL' Missing",
        "env-simulator"
    )
    
    create_log(
        db,
        "ERROR",
        "Configuration Error: Missing API_KEY",
        "env-simulator"
    )
    
    create_log(
        db,
        "CRITICAL",
        "Authentication Failed: Required credentials not found",
        "env-simulator"
    )
    
    create_log(
        db,
        "ERROR",
        "Service Startup Failed: Missing configuration",
        "env-simulator"
    )
    
    return {
        "status": "missing-env injected",
        "logs_generated": 4
    }


# ============================================================================
# File: backend/routes/inject_exception.py (NEW FILE)
# ============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from services.log_service import create_log

router = APIRouter(prefix="/inject")


@router.post("/null-pointer")
def null_pointer(db: Session = Depends(get_db)):
    """
    Simulate null pointer and runtime exceptions
    Module 9 requirement
    """
    create_log(
        db,
        "ERROR",
        "NullPointerException: Object reference not set to an instance",
        "exception-simulator"
    )
    
    create_log(
        db,
        "ERROR",
        "AttributeError: 'NoneType' object has no attribute 'value'",
        "exception-simulator"
    )
    
    create_log(
        db,
        "ERROR",
        "TypeError: Cannot read property of undefined",
        "exception-simulator"
    )
    
    create_log(
        db,
        "CRITICAL",
        "Unhandled Exception: Application Crashed",
        "exception-simulator"
    )
    
    create_log(
        db,
        "INFO",
        "Service Restarted After Crash",
        "exception-simulator"
    )
    
    return {
        "status": "null-pointer injected",
        "logs_generated": 5
    }


# ============================================================================
# File: backend/routes/inject_slow.py (NEW FILE)
# ============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import time

from database.db import get_db
from services.log_service import create_log

router = APIRouter(prefix="/inject")


@router.post("/slow-response")
def slow_response(db: Session = Depends(get_db)):
    """
    Simulate slow response and timeout issues
    Additional requirement
    """
    # Simulate actual slow operation
    time.sleep(3)
    
    create_log(
        db,
        "WARNING",
        "Response Time: 3000ms (Threshold Exceeded: 500ms)",
        "performance-simulator"
    )
    
    create_log(
        db,
        "WARNING",
        "Database Query Slow: 2500ms execution time",
        "performance-simulator"
    )
    
    create_log(
        db,
        "ERROR",
        "Request Timeout: Operation exceeded maximum allowed time",
        "performance-simulator"
    )
    
    create_log(
        db,
        "ERROR",
        "Client Disconnected: Slow response caused timeout",
        "performance-simulator"
    )
    
    return {
        "status": "slow-response injected",
        "simulated_delay": "3000ms",
        "logs_generated": 4
    }


# ============================================================================
# File: backend/main.py (UPDATE - Register new routers)
# ============================================================================

"""
Add these imports and router registrations to main.py:
"""

# Add to imports:
from routes.inject_env import router as env_router
from routes.inject_exception import router as exception_router
from routes.inject_slow import router as slow_router

# Add to app registrations (after existing routers):
app.include_router(env_router)
app.include_router(exception_router)
app.include_router(slow_router)


# ============================================================================
# SUMMARY OF CHANGES NEEDED
# ============================================================================

"""
Files to UPDATE:
1. backend/routes/logs.py
   - Add GET /failures endpoint
   - Add GET /status endpoint

Files to CREATE:
2. backend/routes/inject_env.py (missing-env simulator)
3. backend/routes/inject_exception.py (null-pointer simulator)
4. backend/routes/inject_slow.py (slow-response simulator)

Files to UPDATE:
5. backend/main.py
   - Import new routers
   - Register new routers

Total Time: ~30 minutes
Priority: High for /failures and /status (Member 1 compatibility)
"""
