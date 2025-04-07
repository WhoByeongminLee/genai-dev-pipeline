# agent/api/v1/scene01_endpoints.py

from fastapi import APIRouter, HTTPException
from agent.schema.scene01.request import Scene01Request
from agent.schema.scene01.response import Scene01Response
from agent.orchestrator.scene01_orchestrator import Scene01Orchestrator

router = APIRouter()

@router.post("/scene01/generate", response_model=Scene01Response)
async def generate_scene01_message(request: Scene01Request) -> Scene01Response:
    """
    Scene01 - 마케팅 메시지 자동 생성 엔드포인트
    """
    try:
        orchestrator = Scene01Orchestrator()
        return await orchestrator.run(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"에러 발생: {str(e)}")
