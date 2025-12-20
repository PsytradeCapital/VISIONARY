from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(
    title="Visionary AI Personal Scheduler - Simple Mode",
    description="AI-powered personal scheduling assistant (Demo Mode)",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Visionary AI Personal Scheduler API - Simple Mode",
        "status": "running",
        "features": [
            "Image Gallery Available",
            "Frontend Demo Mode",
            "Design Analysis Tools"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "simple"}

@app.get("/api/demo")
async def demo_data():
    """Return demo data for frontend testing"""
    return {
        "images": [
            {
                "id": "image2",
                "title": "Schedule Planning",
                "rating": 4.8,
                "category": "Scheduling"
            },
            {
                "id": "image4", 
                "title": "AI Assistant",
                "rating": 4.7,
                "category": "AI Assistant"
            },
            {
                "id": "image3",
                "title": "Progress Tracking", 
                "rating": 4.6,
                "category": "Analytics"
            }
        ],
        "stats": {
            "total_images": 19,
            "average_rating": 4.6,
            "categories": 8
        }
    }

@app.get("/docs-redirect")
async def docs_redirect():
    """Redirect to API documentation"""
    return HTMLResponse("""
    <html>
        <head>
            <title>Visionary API - Simple Mode</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
                .header { color: #2c3e50; text-align: center; margin-bottom: 30px; }
                .status { background: #27ae60; color: white; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
                .links { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
                .link-card { background: #3498db; color: white; padding: 20px; border-radius: 8px; text-decoration: none; text-align: center; }
                .link-card:hover { background: #2980b9; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎨 Visionary AI Personal Scheduler</h1>
                    <p>Backend API - Simple Mode</p>
                </div>
                
                <div class="status">
                    ✅ Backend is running successfully!
                </div>
                
                <h3>Available Features:</h3>
                <ul>
                    <li>✅ API Server Running</li>
                    <li>✅ CORS Configured for Frontend</li>
                    <li>✅ Demo Data Endpoints</li>
                    <li>✅ Health Check Available</li>
                </ul>
                
                <div class="links">
                    <a href="http://localhost:3000" class="link-card">
                        <h4>🎨 Frontend App</h4>
                        <p>Main Application</p>
                    </a>
                    <a href="/api/demo" class="link-card">
                        <h4>📊 Demo Data</h4>
                        <p>Sample API Response</p>
                    </a>
                </div>
                
                <h3>Next Steps:</h3>
                <ol>
                    <li>Keep this backend running</li>
                    <li>Open a new terminal</li>
                    <li>Run: <code>start-frontend.bat</code></li>
                    <li>Visit: <a href="http://localhost:3000">http://localhost:3000</a></li>
                </ol>
            </div>
        </body>
    </html>
    """)

if __name__ == "__main__":
    print("🚀 Starting Visionary Backend - Simple Mode")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📖 Visit http://localhost:8000/docs-redirect for info")
    print("🎨 Start frontend with: start-frontend.bat")
    print("")
    
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )