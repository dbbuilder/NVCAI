#!/usr/bin/env python3
"""
NVC AI Facilitator - Railway Deployment Entry Point
"""

import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Add the backend directory to Python path
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        logger.info(f"Backend path: {backend_path}")
        
        if not os.path.exists(backend_path):
            logger.error(f"Backend directory not found: {backend_path}")
            sys.exit(1)
            
        sys.path.insert(0, backend_path)
        
        # Change to backend directory
        os.chdir(backend_path)
        logger.info(f"Changed to directory: {os.getcwd()}")
        
        # Get port from environment (Railway sets this)
        port = int(os.getenv("PORT", 8000))
        logger.info(f"Starting server on port: {port}")
        
        # Import and run the FastAPI app directly
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()