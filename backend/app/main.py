"""
JARVIS Backend Application Entry Point.
Provides FastAPI REST / WebSocket endpoints and background agent orchestrator.
"""
from fastapi import FastAPI

app = FastAPI(
    title="JARVIS AI Agent API",
    description="Backend API and Agent Engine for JARVIS on Ubuntu",
    version="1.0.0",
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "JARVIS Backend", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
