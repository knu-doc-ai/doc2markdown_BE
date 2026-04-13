import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.api.documents import router as documents_router

app = FastAPI(title="DtoM Backend API", version="1.0.0")

# 배포 환경을 고려한 CORS 설정: 로컬 우선 설정 후 환경변수를 통한 덮어쓰기 가능
origins_env = os.getenv("FE_CORS_ORIGINS", "http://localhost:5173")
CORS_ORIGINS = [orig.strip() for orig in origins_env.split(",") if orig.strip()]

# Setup CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # Allow frontend origin via ENV
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the modular routers
app.include_router(api_router, prefix="/api")
app.include_router(documents_router)

@app.get("/health", tags=["Health"])
def health_check():
    """Basic healthcheck endpoint to verify server is running."""
    return {"status": "ok", "message": "Backend server is running"}

if __name__ == "__main__":
    import uvicorn
    # This allows running 'python main.py' directly, but it's usually better to run via CLI
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
