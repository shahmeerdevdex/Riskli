from fastapi import APIRouter
from app.api.v1.endpoints import risk

api_router = APIRouter()
api_router.include_router(risk.router, prefix="/risk", tags=["Risk Analysis"])
