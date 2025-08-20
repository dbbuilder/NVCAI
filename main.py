#!/usr/bin/env python3
"""
NVC AI Facilitator - Railway Deployment Entry Point
This file helps Railway detect this as a Python application.
"""

import sys
import os

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

if __name__ == "__main__":
    # Change to backend directory
    os.chdir(backend_path)
    
    # Get port from environment (Railway sets this)
    port = int(os.getenv("PORT", 8000))
    
    # Import and run the FastAPI app directly
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )