from pydantic import BaseModel, Field
from typing import Dict, Any

class RiskAnalysisRequest(BaseModel):
    data: Dict[str, str]


