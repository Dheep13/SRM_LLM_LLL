"""
FastAPI API Routes
Defines REST API endpoints for LawBot
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from backend.services.lawbot_service import LawBotService

logger = logging.getLogger(__name__)
router = APIRouter()

# Global service instance
lawbot_service = LawBotService()

# Pydantic models
class ChatRequest(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    response: str
    citations: List[str]
    tools_used: List[Dict[str, Any]]
    confidence: str
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    components: Dict[str, Any]

class ToolLookupRequest(BaseModel):
    tool_type: str
    query: str
    parameters: Optional[Dict[str, Any]] = None

# Dependency to get service
def get_lawbot_service():
    return lawbot_service

@router.post("/chat", response_model=ChatResponse)
async def chat_with_lawbot(
    request: ChatRequest,
    service: LawBotService = Depends(get_lawbot_service)
):
    """Chat with LawBot - main endpoint"""
    try:
        result = service.chat(request.query, request.conversation_history)
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check(service: LawBotService = Depends(get_lawbot_service)):
    """Health check endpoint"""
    try:
        status = service.get_system_status()
        return HealthResponse(
            status="healthy" if status["is_initialized"] else "degraded",
            components=status
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_model_status(service: LawBotService = Depends(get_lawbot_service)):
    """Get model status and information"""
    try:
        status = service.get_system_status()
        return {
            "model": status["model"],
            "rag": status["rag"],
            "tools": status["tools"]
        }
    except Exception as e:
        logger.error(f"Model status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tools/lookup")
async def lookup_tool(
    request: ToolLookupRequest,
    service: LawBotService = Depends(get_lawbot_service)
):
    """Use specific tools"""
    try:
        tools_manager = service.tools_manager
        
        if request.tool_type == "legal_dictionary":
            result = tools_manager.lookup_legal_term(request.query)
        elif request.tool_type == "date_calculator":
            days = request.parameters.get("days", 30) if request.parameters else 30
            start_date = request.parameters.get("start_date") if request.parameters else None
            result = tools_manager.calculate_deadline(days, start_date)
        elif request.tool_type == "case_lookup":
            result = tools_manager.lookup_legal_case(request.query)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool type: {request.tool_type}")
        
        return result
        
    except Exception as e:
        logger.error(f"Tool lookup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools/info")
async def get_tools_info(service: LawBotService = Depends(get_lawbot_service)):
    """Get available tools information"""
    try:
        return service.tools_manager.get_tools_info()
    except Exception as e:
        logger.error(f"Tools info error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
