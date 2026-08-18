from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import auth, jobs
# from .api.endpoints import jobs   

# Create the FastAPI application instance
app = FastAPI(
    title="Voxora API",
    description="The backend API for the Voxora application.",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTERS ---
# Include the authentication router
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

# --- ROOT ENDPOINT ---
@app.get("/")
def read_root():
    """
    Root healthcheck endpoint.
    """
    return {"status": "ok", "message": "Welcome to the Voxora API!"}