from fastapi import FastAPI, Query, HTTPException, Depends, status # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # type: ignore
from fastapi.params import Body # type: ignore
from datetime import timedelta
from jose import JWTError, jwt # type: ignore
import logging
from services.auth import authenticate_user, create_access_token
from services.images import get_images, update_image  # ✅ Import services

app = FastAPI()

# Configure CORS
origins = ["http://localhost:5173", "http://localhost:8000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key and algorithm for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint to generate access token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token({"sub": user["username"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decode JWT token to get current user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    """A protected route that requires authentication."""
    return {"message": f"Welcome {username}!"}

@app.get("/data")
async def read_images(
    search: str = Query(default=None), page: int = Query(default=1), page_size: int = Query(default=10), username: str = Depends(get_current_user)
):
    """API Route to fetch images with pagination and search."""
    logger.info(f"📌 GET /data - Search: {search} | Page: {page} | Page Size: {page_size}")
    result = get_images(search, page, page_size)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

# create a post API in order to post images:
@app.post("/create-upload")
def create_upload(payload: dict = Body(...)):
    print(payload)
    return {f"title: {payload['title']}, description: {payload['description']}"}


@app.put("/update/{image_id}")
async def modify_image(image_id: str, image: dict):
    """API Route to update image details."""
    logger.info(f"📌 PUT /update/{image_id} - Updating image")
    result = update_image(image_id, image)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result
