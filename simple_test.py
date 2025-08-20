#!/usr/bin/env python3
"""
Simple test server to debug Railway deployment issues
"""
import os
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Simple Test")

@app.get("/")
def root():
    return {"status": "ok", "message": "Simple test server is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/debug")
def debug():
    return {
        "cwd": os.getcwd(),
        "files": os.listdir("."),
        "env_port": os.getenv("PORT", "not_set"),
        "python_path": os.getenv("PYTHONPATH", "not_set")
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting simple test server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)