"""
NVC resources and guidance API endpoints
"""
from fastapi import APIRouter

router = APIRouter()

# TODO: Implement NVC resource endpoints
@router.get("/feelings")
async def get_feelings_list():
    """Get list of NVC feelings vocabulary."""
    return {"message": "Get feelings list endpoint - TODO"}

@router.get("/needs")
async def get_needs_list():
    """Get list of universal human needs."""
    return {"message": "Get needs list endpoint - TODO"}

@router.get("/examples")
async def get_nvc_examples():
    """Get NVC practice examples."""
    return {"message": "Get NVC examples endpoint - TODO"}