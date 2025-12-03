from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import youtube, settings

app = FastAPI(
    title="YouTube Analytics API",
    description="Backend API for YouTube video search and analytics",
    version="1.0.0"
)

# CORS configuration for Nuxt frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Nuxt dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(youtube.router)
app.include_router(settings.router)

@app.get("/")
async def root():
    return {
        "message": "YouTube Analytics API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
