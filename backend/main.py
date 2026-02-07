from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from database import init_db
from auth import verify_token
from api.upload import router as upload_router
from api.schedule import router as schedule_router
from api.reminders import router as reminders_router
from api.progress import router as progress_router
from api.websocket import router as websocket_router
from api.auth import router as auth_router

# Railway deployment version 1.0
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    try:
        await init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
        print("📝 Using in-memory fallback mode")
    
    print("🚀 Visionary Backend Started Successfully!")
    print("📍 API available at: http://localhost:8000")
    print("📖 API docs at: http://localhost:8000/docs")
    yield

app = FastAPI(
    title="Visionary AI Personal Scheduler",
    description="AI-powered personal scheduling assistant",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(schedule_router)
app.include_router(reminders_router)
app.include_router(progress_router)
app.include_router(websocket_router)

@app.get("/")
async def root():
    return {"message": "Visionary AI Personal Scheduler API"}

@app.get("/api/")
async def api_root():
    return {"message": "Visionary AI API v1.0", "status": "operational"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Example protected route requiring authentication"""
    user = await verify_token(credentials.credentials)
    return {"message": f"Hello {user['email']}", "user_id": user["id"]}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )