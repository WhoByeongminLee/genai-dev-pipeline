# agent/schema/scene01/response.py

from pydantic import BaseModel, Field
from typing import List




class GeneratedMessage(BaseModel):
    channel: str = Field(..., description="해당 발송 채널 (PUSH, 알림톡, LMS 등)")
    content: str = Field(..., description="생성된 마케팅 메시지")


class Scene01Response(BaseModel):
    result: str
    used_prompt: str

"""
class Scene01Response(BaseModel):
    messages: List[GeneratedMessage] = Field(..., description="각 채널별 생성된 마케팅 메시지 목록")
    used_prompt: str = Field(..., description="LLM 요청에 사용된 최종 프롬프트")
"""
