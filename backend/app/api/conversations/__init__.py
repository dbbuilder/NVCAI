"""
Conversation management API endpoints
"""
from fastapi import APIRouter

router = APIRouter()

# TODO: Implement conversation endpoints
@router.post("/")
async def create_conversation():
    """Create a new NVC conversation session."""
    return {"message": "Create conversation endpoint - TODO"}

@router.get("/{conversation_id}")
async def get_conversation():
    """Get conversation by ID."""
    return {"message": "Get conversation endpoint - TODO"}

@router.post("/{conversation_id}/messages")
async def send_message():
    """Send message in conversation."""
    return {"message": "Send message endpoint - TODO"}