from fastapi import FastAPI
from app.api import survey
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings

# Initialize FastAPI app
app = FastAPI(
    title="AI Tutor API",
    description="API for personalized JavaScript learning experience",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(survey.router, prefix="/api")

@app.get("/")
async def root():
    """
    Root endpoint returning API information
    """
    return {
        "message": "Welcome to AI Tutor API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "api_version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)