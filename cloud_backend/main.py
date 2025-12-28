"""
Visionary AI Personal Scheduler - Cloud Backend
FastAPI application with cloud-native architecture
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.core.database import init_db
from app.core.redis_client import init_redis
from app.api.v1 import api_router
from app.core.auth import verify_token

load_dotenv()

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await init_redis()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Visionary AI Personal Scheduler",
    description="Cloud-native AI-powered personal scheduling assistant",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for mobile and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancer"""
    return {"status": "healthy", "service": "visionary-backend"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Visionary AI Personal Scheduler API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    )