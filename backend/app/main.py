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


@app.get("/", response_class=Response)
async def root():
    """Root endpoint with basic API information and UI link."""
    html_content = f"""
    <html>
    <head><title>NVC AI Facilitator</title></head>
    <body style="font-family: Arial, sans-serif; margin: 40px; text-align: center;">
        <h1>🤝 NVC AI Facilitator</h1>
        <p>Version: {settings.APP_VERSION}</p>
        <p><strong>API Endpoints:</strong></p>
        <ul style="display: inline-block; text-align: left;">
            <li><a href="/health">Health Check</a></li>
            <li><a href="{settings.API_V1_STR}/docs">API Documentation</a></li>
            <li><a href="/test">Web Interface</a> (if deployed)</li>
        </ul>
        <hr>
        <h2>Quick Test</h2>
        <textarea id="msg" placeholder="Try: I'm frustrated with my coworker" style="width: 300px; height: 60px;"></textarea><br><br>
        <button onclick="testAPI()" style="padding: 10px 20px; font-size: 16px;">Get NVC Guidance</button>
        <div id="result" style="margin-top: 20px; padding: 20px; background: #f0f0f0; border-radius: 10px; display: none;"></div>
        
        <script>
        async function testAPI() {{
            const msg = document.getElementById('msg').value;
            if (!msg) return;
            
            const result = document.getElementById('result');
            result.style.display = 'block';
            result.innerHTML = 'Processing...';
            
            try {{
                const response = await fetch('{settings.API_V1_STR}/nvc/conversation', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ message: msg, conversation_history: [] }})
                }});
                const data = await response.json();
                result.innerHTML = `
                    <strong>AI Response:</strong> ${{data.ai_response}}<br>
                    <strong>Guidance:</strong> ${{data.guidance}}<br>
                    <strong>NVC Step:</strong> ${{data.suggested_nvc_step}}
                `;
            }} catch (error) {{
                result.innerHTML = `Error: ${{error.message}}`;
            }}
        }}
        </script>
    </body>
    </html>
    """
    return Response(content=html_content, media_type="text/html")


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