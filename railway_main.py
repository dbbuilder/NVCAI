#!/usr/bin/env python3
"""
Simplified Railway deployment entry point - bypasses complex directory structure
"""
import os
import sys
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Change to backend directory for imports
os.chdir(str(backend_path))

# Import and run the app
if __name__ == "__main__":
    from app.main import app
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    print(f"[RAILWAY] Starting on 0.0.0.0:{port}")
    print(f"[RAILWAY] Environment PORT = {os.getenv('PORT', 'NOT_SET')}")
    
    uvicorn.run(
        app,  # Use the app object directly
        host="0.0.0.0",
        port=port,
        log_level="info"
    )