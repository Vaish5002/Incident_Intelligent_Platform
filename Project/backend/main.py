"""
SmartOps AI - RCA Engine (Member 3)
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from ai.config import settings
from api.rca_routes import router as rca_router
from api.risk_routes import router as risk_router
from api.knowledge_routes import router as knowledge_router
from api.rag_routes import router as rag_router
from api.copilot_routes import router as copilot_router
from api.pdf_routes import router as pdf_router
from api.integration_routes import router as integration_router
from api.demo_investigate_routes import router as demo_router
from api.full_investigation_routes import router as full_router

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO" if not settings.DEBUG else "DEBUG"
)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Root Cause Analysis Engine for SmartOps Platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS - Allow all origins for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=False,  # Must be False when allow_origins is "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - Demo investigation first (takes precedence)
app.include_router(full_router)  # FULL investigation with ALL agents
app.include_router(demo_router)  # Demo investigation endpoint
app.include_router(rca_router)
app.include_router(risk_router)
app.include_router(knowledge_router)
app.include_router(rag_router)
app.include_router(copilot_router)
app.include_router(pdf_router)
app.include_router(integration_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Member 3 - AI & RCA Engine",
        "member": "Member 3",
        "responsibilities": [
            "Groq Integration",
            "RAG System",
            "RCA Generation",
            "Risk Scoring",
            "Knowledge Base",
            "Embedding Service",
            "RAG Retrieval",
            "AI Copilot",
            "PDF Generation"
        ],
        "endpoints": {
            "health": "/api/health",
            "generate_rca": "POST /api/generate-rca",
            "quick_rca": "POST /api/quick-rca",
            "recommendations": "POST /api/recommendations",
            "docs": "/docs"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Automatically initialize database tables if they do not exist
    try:
        from backend.database.connection import init_db
        init_db()
    except Exception as db_err:
        logger.error(f"Failed to auto-initialize database on startup: {db_err}")

    logger.info(f"Groq Model: {settings.GROQ_MODEL}")
    logger.info(f"Server ready on {settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"Documentation: http://{settings.API_HOST}:{settings.API_PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down SmartOps AI RCA Engine")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
