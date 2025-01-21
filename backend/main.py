from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from routes import auth, images, protected  # Import routes

app = FastAPI()

# Configure CORS
origins = ["http://localhost:5173", "http://localhost:8000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(images.router, prefix="/images", tags=["Images"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app!"}
