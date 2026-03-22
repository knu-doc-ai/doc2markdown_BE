from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/status")
def get_status():
    return {"status": "ok", "message": "API Router is successfully initialized"}
