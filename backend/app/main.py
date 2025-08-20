"""
NVC AI Facilitator - Main FastAPI Application
Provides AI-powered Non-Violent Communication facilitation
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from loguru import logger
import os

from app.core.config import settings
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info("Starting NVC AI Facilitator application")
    
    yield
    
    # Shutdown
    logger.info("Shutting down NVC AI Facilitator application")


# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Non-Violent Communication facilitation platform",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# CORS middleware - Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve the test UI
@app.get("/test")
async def serve_test_ui():
    """Serve the test UI HTML file."""
    # Look for test_ui.html in the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    test_ui_path = os.path.join(project_root, "test_ui.html")
    
    logger.info(f"Looking for test UI at: {test_ui_path}")
    
    if os.path.exists(test_ui_path):
        return FileResponse(test_ui_path, media_type="text/html")
    else:
        # Fallback paths
        fallback_paths = [
            "test_ui.html",
            "../test_ui.html", 
            "../../test_ui.html",
            "/app/test_ui.html"
        ]
        
        for fallback_path in fallback_paths:
            if os.path.exists(fallback_path):
                logger.info(f"Found test UI at fallback path: {fallback_path}")
                return FileResponse(fallback_path, media_type="text/html")
        
        return JSONResponse({
            "error": "Test UI file not found", 
            "searched_paths": [test_ui_path] + fallback_paths,
            "current_dir": os.getcwd(),
            "files_in_current_dir": os.listdir(".")
        }, status_code=404)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_id": "Please contact support with this error ID"
        }
    )


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/")
async def root():
    """Root endpoint - serve the full NVC UI directly."""
    # Serve the same UI as /test endpoint at the root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    test_ui_path = os.path.join(project_root, "test_ui.html")
    
    logger.info(f"Root endpoint looking for UI at: {test_ui_path}")
    
    if os.path.exists(test_ui_path):
        return FileResponse(test_ui_path, media_type="text/html")
    else:
        # Fallback paths
        fallback_paths = [
            "test_ui.html",
            "../test_ui.html", 
            "../../test_ui.html",
            "/app/test_ui.html"
        ]
        
        for fallback_path in fallback_paths:
            if os.path.exists(fallback_path):
                logger.info(f"Root endpoint found UI at fallback path: {fallback_path}")
                return FileResponse(fallback_path, media_type="text/html")
        
        # If no UI file found, return basic info
        return JSONResponse({
            "message": "NVC AI Facilitator API",
            "version": settings.APP_VERSION,
            "docs_url": f"{settings.API_V1_STR}/docs",
            "error": "UI file not found - showing API info instead"
        })


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 19000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )