from fastapi import FastAPI, Query, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import logging
from services import get_images, update_image  # ✅ Import services

app = FastAPI()

# Configure CORS
origins = ["http://localhost:5173", "http://localhost:8000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@app.get("/data")
async def read_images(
    search: str = Query(default=None), page: int = Query(default=1), page_size: int = Query(default=10)
):
    """API Route to fetch images with pagination and search."""
    logger.info(f"📌 GET /data - Search: {search} | Page: {page} | Page Size: {page_size}")
    result = get_images(search, page, page_size)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.put("/update/{image_id}")
async def modify_image(image_id: str, image: dict):
    """API Route to update image details."""
    logger.info(f"📌 PUT /update/{image_id} - Updating image")
    result = update_image(image_id, image)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result
