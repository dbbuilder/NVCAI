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
@app.get("/test", response_class=Response)
async def serve_test_ui():
    """Serve the embedded test UI."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NVC AI Facilitator - Test Interface</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            padding: 20px;
        }
        .container {
            background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%; max-width: 800px; overflow: hidden;
        }
        .header {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; padding: 30px; text-align: center;
        }
        .content { padding: 30px; }
        .input-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
        textarea, input {
            width: 100%; padding: 12px; border: 2px solid #e1e5e9;
            border-radius: 10px; font-size: 16px; transition: border-color 0.3s;
        }
        textarea:focus, input:focus { outline: none; border-color: #667eea; }
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; border: none; padding: 12px 30px; border-radius: 10px;
            font-size: 16px; cursor: pointer; transition: transform 0.2s;
        }
        .btn:hover { transform: translateY(-2px); }
        .response { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px; }
        .nvc-step { display: inline-block; background: #667eea; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; margin-bottom: 10px; }
        .suggestions { margin-top: 15px; }
        .suggestion-btn {
            display: inline-block; background: #e3f2fd; color: #1976d2; border: none;
            padding: 8px 16px; margin: 4px; border-radius: 20px; cursor: pointer; font-size: 14px;
        }
        .suggestion-btn:hover { background: #bbdefb; }
        .vocabulary { margin-top: 10px; }
        .vocab-tag {
            display: inline-block; background: #f1f3f4; color: #5f6368;
            padding: 4px 8px; margin: 2px; border-radius: 12px; font-size: 12px;
        }
        .nvc-summary { background: #e8f5e8; border-left: 4px solid #4caf50; padding: 20px; margin-top: 20px; border-radius: 0 10px 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤝 NVC AI Facilitator</h1>
            <p>Your AI guide for Non-Violent Communication practice</p>
        </div>
        <div class="content">
            <div class="input-group">
                <label for="message">Share your situation:</label>
                <textarea id="message" rows="4" placeholder="Describe what's happening or how you're feeling..."></textarea>
            </div>
            <button class="btn" onclick="sendMessage()">Get NVC Guidance</button>
            <button class="btn" onclick="clearConversation()" style="background: #6c757d; margin-left: 10px;">Clear</button>
            <div id="response"></div>
        </div>
    </div>

    <script>
        let conversationHistory = [];
        const API_BASE = window.location.origin;

        async function sendMessage() {
            const message = document.getElementById('message').value.trim();
            if (!message) return;

            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = '<p>🤔 Processing your message...</p>';

            try {
                const response = await fetch(`${API_BASE}/api/v1/nvc/conversation`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message, conversation_history: conversationHistory })
                });

                const data = await response.json();
                conversationHistory.push({ user: message, ai: data.ai_response });

                displayResponse(data);
                document.getElementById('message').value = '';
            } catch (error) {
                responseDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            }
        }

        function displayResponse(data) {
            const responseDiv = document.getElementById('response');
            
            let html = `
                <div class="response">
                    <div class="nvc-step">NVC Step: ${data.suggested_nvc_step?.toUpperCase() || 'GUIDANCE'}</div>
                    <h3>AI Response:</h3>
                    <p><strong>${data.ai_response}</strong></p>
                    <p><em>${data.guidance}</em></p>
            `;

            if (data.suggested_responses?.length > 0) {
                html += `<div class="suggestions"><strong>Try saying:</strong><br>`;
                data.suggested_responses.forEach(suggestion => {
                    html += `<button class="suggestion-btn" onclick="useSuggestion('${suggestion.replace(/'/g, '&apos;')}')">${suggestion}</button>`;
                });
                html += `</div>`;
            }

            if (data.vocabulary_options?.length > 0) {
                html += `<div class="vocabulary"><strong>${data.suggested_nvc_step} vocabulary:</strong><br>`;
                data.vocabulary_options.forEach(word => {
                    html += `<span class="vocab-tag">${word}</span>`;
                });
                html += `</div>`;
            }

            if (data.nvc_summary) {
                html += `<div class="nvc-summary"><strong>🎯 NVC Summary:</strong><br>${data.nvc_summary.replace(/\\n/g, '<br>')}</div>`;
            }

            html += `</div>`;
            responseDiv.innerHTML = html;
        }

        function useSuggestion(suggestion) {
            document.getElementById('message').value = suggestion;
        }

        function clearConversation() {
            conversationHistory = [];
            document.getElementById('response').innerHTML = '';
            document.getElementById('message').value = '';
        }

        document.getElementById('message').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>"""
    return Response(content=html_content, media_type="text/html")


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
async def root() -> dict:
    """Root endpoint with basic API information."""
    return {
        "message": "NVC AI Facilitator API",
        "version": settings.APP_VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs"
    }


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