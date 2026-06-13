"""
AI Copilot API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from loguru import logger

from ai.copilot_service import CopilotService

router = APIRouter(prefix="/api/copilot", tags=["AI Copilot"])

# Initialize Copilot service
try:
    copilot_service = CopilotService()
    logger.info("Copilot service initialized for API")
except Exception as e:
    logger.error(f"Failed to initialize Copilot service: {e}")
    copilot_service = None


# Request/Response Models
class AskRequest(BaseModel):
    """Request for asking copilot a question"""
    question: str
    context: Optional[Dict[str, Any]] = None
    use_history: bool = True


class ExplainRCARequest(BaseModel):
    """Request for explaining RCA"""
    rca_text: str
    focus: Optional[str] = None  # root_cause, impact, recommendations, prevention


class NextStepsRequest(BaseModel):
    """Request for suggesting next steps"""
    incident: str
    current_status: str
    actions_taken: Optional[List[str]] = None


class CompareSimilarRequest(BaseModel):
    """Request for comparing with similar incidents"""
    current_incident: str
    logs: Optional[str] = None


@router.post("/ask")
async def ask_copilot(request: AskRequest):
    """
    Ask the AI Copilot a question
    
    **Test 1 Requirement:** Ask "Why did this happen?" → Answer uses RCA context
    
    Supported questions:
    - Why did this happen?
    - Which commit caused this?
    - How do we prevent this?
    - What should we do next?
    - Explain the root cause
    - What do the logs tell us?
    
    Example:
    ```json
    {
      "question": "Why did this happen?",
      "context": {
        "incident": "Payment failures",
        "rca_text": "Database pool size was reduced...",
        "severity": "Critical"
      },
      "use_history": true
    }
    ```
    
    Response:
    ```json
    {
      "success": true,
      "answer": "Based on the RCA, this happened because...",
      "question": "Why did this happen?",
      "question_type": "causality",
      "used_context": true
    }
    ```
    """
    if not copilot_service:
        raise HTTPException(status_code=503, detail="Copilot service not available")
    
    try:
        result = copilot_service.ask(
            question=request.question,
            context=request.context,
            use_history=request.use_history
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in copilot ask: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain-rca")
async def explain_rca(request: ExplainRCARequest):
    """
    Explain an RCA in simpler terms
    
    Converts technical RCA into easy-to-understand explanation.
    
    Optional focus areas:
    - root_cause: Explain the root cause
    - impact: Explain the impact
    - recommendations: Explain the recommendations
    - prevention: Explain prevention measures
    - (none): Explain entire RCA
    """
    if not copilot_service:
        raise HTTPException(status_code=503, detail="Copilot service not available")
    
    try:
        result = copilot_service.explain_rca(
            rca_text=request.rca_text,
            focus=request.focus
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error explaining RCA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest-next-steps")
async def suggest_next_steps(request: NextStepsRequest):
    """
    Suggest next steps for incident resolution
    
    Based on current incident status and actions taken,
    provides intelligent suggestions for next steps.
    """
    if not copilot_service:
        raise HTTPException(status_code=503, detail="Copilot service not available")
    
    try:
        result = copilot_service.suggest_next_steps(
            incident=request.incident,
            current_status=request.current_status,
            actions_taken=request.actions_taken
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error suggesting next steps: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare-similar")
async def compare_with_similar(request: CompareSimilarRequest):
    """
    Compare current incident with similar historical incidents
    
    Uses RAG to find similar incidents and provides comparison insights.
    """
    if not copilot_service:
        raise HTTPException(status_code=503, detail="Copilot service not available")
    
    try:
        result = copilot_service.compare_with_similar(
            current_incident=request.current_incident,
            logs=request.logs
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error comparing with similar: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear-history")
async def clear_history():
    """
    Clear conversation history
    
    Resets the copilot's memory of previous questions.
    """
    if not copilot_service:
        raise HTTPException(status_code=503, detail="Copilot service not available")
    
    try:
        copilot_service.clear_history()
        return {
            "success": True,
            "message": "Conversation history cleared"
        }
        
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_history():
    """
    Get conversation history
    
    Returns list of previous question-answer pairs.
    """
    if not copilot_service:
        raise HTTPException(status_code=503, detail="Copilot service not available")
    
    try:
        history = copilot_service.get_history()
        return {
            "success": True,
            "history": history,
            "count": len(history)
        }
        
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggested-questions")
async def get_suggested_questions(context: Optional[Dict[str, Any]] = None):
    """
    Get suggested questions based on context
    
    Returns a list of relevant questions user might want to ask.
    """
    if not copilot_service:
        raise HTTPException(status_code=503, detail="Copilot service not available")
    
    try:
        suggestions = copilot_service.get_suggested_questions(context=context)
        return {
            "success": True,
            "suggestions": suggestions,
            "count": len(suggestions)
        }
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_copilot_info():
    """
    Get copilot service information
    
    Returns service status and capabilities.
    """
    if not copilot_service:
        raise HTTPException(status_code=503, detail="Copilot service not available")
    
    try:
        info = copilot_service.get_service_info()
        return info
        
    except Exception as e:
        logger.error(f"Error getting copilot info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def copilot_health_check():
    """
    Health check for copilot service
    """
    if not copilot_service:
        return {
            "status": "unhealthy",
            "service": "AI Copilot",
            "error": "Service not initialized"
        }
    
    try:
        info = copilot_service.get_service_info()
        return {
            "status": "healthy",
            "service": "AI Copilot",
            "ai_model": info.get("ai_model"),
            "conversation_size": info.get("conversation_history_size")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "AI Copilot",
            "error": str(e)
        }
