"""
API router configuration
"""
from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.conversations import router as conversations_router
from app.api.nvc import router as nvc_router
from app.api.research import router as research_router

api_router = APIRouter()

# Include all API routes
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(conversations_router, prefix="/conversations", tags=["conversations"])
api_router.include_router(nvc_router, prefix="/nvc", tags=["nvc"])
api_router.include_router(research_router, prefix="/research", tags=["research"])