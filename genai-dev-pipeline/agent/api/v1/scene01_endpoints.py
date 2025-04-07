# agent/api/v1/scene01_endpoints.py

from fastapi import APIRouter, HTTPException
from agent.schema.scene01.request import Scene01Request
from agent.schema.scene01.response import Scene01Response
from agent.orchestrator.scene01_orchestrator import Scene01Orchestrator
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/scene01/generate", response_model=Scene01Response)
async def generate_scene01_message(request: Scene01Request) -> Scene01Response:
    """
    Scene01 - 마케팅 메시지 자동 생성 엔드포인트
    """
    try:
        orchestrator = Scene01Orchestrator()
        response = await orchestrator.run(request)
        return response
    except Exception as e:
        logger.exception(f"Scene01 생성 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="마케팅 메시지 생성 중 오류가 발생했습니다.")
