from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router

app = FastAPI(title="DtoM Backend API", version="1.0.0")

# Setup CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the modular routers
app.include_router(api_router, prefix="/api")

@app.get("/health", tags=["Health"])
def health_check():
    """Basic healthcheck endpoint to verify server is running."""
    return {"status": "ok", "message": "Backend server is running"}

if __name__ == "__main__":
    import uvicorn
    # This allows running 'python main.py' directly, but it's usually better to run via CLI
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
