from fastapi import APIRouter, Depends # type: ignore
from security.jwt_handler import get_current_user

router = APIRouter()

@router.get("/")
async def protected_route(username: str = Depends(get_current_user)):
    """A protected route that requires authentication."""
    return {"message": f"Welcome {username}!"}
