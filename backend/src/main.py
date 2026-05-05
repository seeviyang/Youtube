"""Main API server for YouTube Analysis Agent System"""

import logging
import json
import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Ensure the backend directory is in the path for proper package resolution
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Now import from src as a package
from src.config import config
from src.orchestrator import VideoAnalysisOrchestrator

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Video Analysis Agent",
    description="Multi-agent system for analyzing YouTube videos",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = VideoAnalysisOrchestrator()

# Request/Response models
class AnalysisRequest(BaseModel):
    """Request model for video analysis"""
    url: str
    use_cache: bool = True


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    ollama_connected: bool
    model: str


class AnalysisResponse(BaseModel):
    """Response model for video analysis"""
    status: str
    data: Optional[dict] = None
    error: Optional[str] = None


# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "name": "YouTube Video Analysis Agent",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health", tags=["Health"], response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    ollama_connected = config.validate_ollama_connection()
    
    if not ollama_connected:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not available"
        )
    
    return HealthResponse(
        status="healthy",
        ollama_connected=ollama_connected,
        model=config.OLLAMA_MODEL
    )


@app.post("/analyze", tags=["Analysis"], response_model=AnalysisResponse)
async def analyze_video(request: AnalysisRequest):
    """
    Analyze a YouTube video
    
    Args:
        request: AnalysisRequest with YouTube URL
        
    Returns:
        AnalysisResponse with complete analysis
    """
    try:
        logger.info(f"Analyzing video: {request.url}")
        
        # Verify Ollama connection
        if not config.validate_ollama_connection():
            raise HTTPException(
                status_code=503,
                detail="Ollama service is not available"
            )
        
        # Perform analysis
        
        result = orchestrator.analyze(request.url)
        
        # Ensure result is JSON serializable
        try:
            json.dumps(result, default=str)
        except (TypeError, ValueError) as e:
            logger.error(f"Result serialization error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to serialize analysis result: {str(e)}"
            )
        
        return AnalysisResponse(
            status="success",
            data=result
        )
    
    except ValueError as e:
        logger.error(f"Invalid URL: {str(e)}")
        return AnalysisResponse(
            status="error",
            error=f"Invalid YouTube URL: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return AnalysisResponse(
            status="error",
            error=f"Analysis failed: {str(e)}"
        )


@app.get("/history", tags=["Memory"])
async def get_analysis_history(limit: int = 10):
    """Get previous analyses"""
    try:
        history = orchestrator.get_previous_analyses(limit)
        return {
            "status": "success",
            "count": len(history),
            "data": history
        }
    except Exception as e:
        logger.error(f"Failed to get history: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


@app.get("/similar/{video_id}", tags=["Memory"])
async def find_similar(video_id: str):
    """Find similar videos to a previously analyzed video"""
    try:
        similar = orchestrator.find_similar_videos(video_id)
        return {
            "status": "success",
            "count": len(similar),
            "data": similar
        }
    except Exception as e:
        logger.error(f"Failed to find similar videos: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


@app.get("/config", tags=["System"])
async def get_config():
    """Get current configuration"""
    return {
        "ollama_url": config.OLLAMA_BASE_URL,
        "model": config.OLLAMA_MODEL,
        "max_tokens": config.MAX_TOKENS,
        "temperature": config.TEMPERATURE,
        "memory_path": config.MEMORY_PATH,
        "transcript_cache": config.TRANSCRIPT_CACHE,
    }


if __name__ == "__main__":
    print(f"""
    🎬 YouTube Video Analysis Agent System
    ==========================================
    
    API Server starting...
    Host: {config.API_HOST}
    Port: {config.API_PORT}
    
    📚 Documentation: http://localhost:{config.API_PORT}/docs
    🔧 ReDoc: http://localhost:{config.API_PORT}/redoc
    
    Make sure Ollama is running:
      ollama serve
    
    Pull a model:
      ollama pull mistral
    """)
    
    # Debug info
    print(f"Python path: {sys.path}")
    print(f"Current working directory: {os.getcwd()}")
    
    uvicorn.run(
        "backend.src.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        log_level=config.LOG_LEVEL.lower(),
        reload=False
    )
