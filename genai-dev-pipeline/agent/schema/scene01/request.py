# agent/schema/scene01/request.py

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from enum import Enum


class MessageType(str, Enum):
    customer = "대고객메시지"
    ad_review = "광고심의문구"
    notice = "유의문구"


class ChannelType(str, Enum):
    push = "PUSH"
    kakao = "알림톡"
    lms = "LMS"


class ChatTurn(BaseModel):
    user: str = Field(..., description="사용자 입력 프롬프트")
    ai: str = Field(..., description="AI가 생성한 응답")


class Scene01Request(BaseModel):
    message_type: MessageType = Field(..., description="메시지 유형")
    life_stage: str = Field(..., description="라이프스테이지 (예: 사회초년생)")
    channels: List[ChannelType] = Field(..., description="발송 채널들")
    prompt: str = Field(..., description="현재 사용자 입력 프롬프트")
    file_url: Optional[str] = None
    # file_url: Optional[HttpUrl] = Field(None, description="기획안 파일 URL (선택)")
    session_id: Optional[str] = Field(None, description="세션 식별자 (히스토리 트래킹 용)")
    history: Optional[List[ChatTurn]] = Field(
        None, description="가장 최근 3개 문답의 히스토리"
    )
