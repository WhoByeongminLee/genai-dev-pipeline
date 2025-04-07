from fastapi import APIRouter, Depends
from agent.schema.scene01.request import MarketingRequest
from agent.schema.scene01.response import MarketingResponse
from agent.orchestrator.scene01_orchestrator import MarketingOrchestrator

router = APIRouter()

def get_orchestrator():
    return MarketingOrchestrator()

@router.post("/scene01/marketing-copy", response_model=MarketingResponse)
async def generate_marketing(
    request: MarketingRequest,
    orchestrator: MarketingOrchestrator = Depends(get_orchestrator)
):
    return await orchestrator.generate_marketing_copy(request)
