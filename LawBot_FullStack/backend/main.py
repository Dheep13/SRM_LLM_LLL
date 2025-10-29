"""
FastAPI Main Application
Entry point for the LawBot backend API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
from backend.api.routes import router
from backend.services.lawbot_service import LawBotService
from config.settings import API_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LawBot API",
    description="Intelligent Legal Q&A Assistant for Indian Law",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Global service instance
lawbot_service = LawBotService()

@app.on_event("startup")
async def startup_event():
    """Initialize LawBot service on startup"""
    logger.info("Starting LawBot API...")
    try:
        success = lawbot_service.initialize()
        if success:
            logger.info("✅ LawBot service initialized successfully!")
        else:
            logger.warning("⚠️ LawBot service initialized in limited mode")
    except Exception as e:
        logger.error(f"❌ Failed to initialize LawBot service: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down LawBot API...")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LawBot API - Intelligent Legal Q&A Assistant",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/status")
async def get_status():
    """Get detailed system status"""
    try:
        status = lawbot_service.get_system_status()
        return {
            "status": "healthy" if status["is_initialized"] else "degraded",
            "components": status,
            "api_version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Status check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["debug"],
        log_level="info"
    )
