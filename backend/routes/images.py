from fastapi import APIRouter, Query, Depends, HTTPException # type: ignore
from controllers.images_controller import get_images, update_image
from security.jwt_handler import get_current_user

router = APIRouter()

@router.get("/")
async def read_images(
    search: str = Query(default=None), 
    page: int = Query(default=1), 
    page_size: int = Query(default=10), 
    username: str = Depends(get_current_user) # to update to the ID
):
    """Fetch images with pagination and search."""
    result = get_images(search, page, page_size)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.put("/{image_id}")
async def modify_image(image_id: str, image: dict):
    """Update an image."""
    result = update_image(image_id, image)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
