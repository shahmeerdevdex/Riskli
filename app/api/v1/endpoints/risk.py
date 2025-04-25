from fastapi import APIRouter, Body
from app.schemas.risk import RiskAnalysisRequest
from app.services.openai_service import generate_risk_analysis
from typing import Dict, Any


router = APIRouter()

@router.post("/risk-analysis")
async def analyze_risk(data: Dict[str, Any] = Body(..., embed=False)):
    return await generate_risk_analysis(data)
