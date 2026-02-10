from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orchestrator.api.routes import chat, health
from orchestrator.middleware.logging import LoggingMiddleware

# Create FastAPI app
app = FastAPI(
    title="AI Memory System Orchestrator",
    description="System orchestrator for AI memory-augmented chat",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(chat.router)
app.include_router(health.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Memory System Orchestrator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
