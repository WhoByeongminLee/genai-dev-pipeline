# agent/orchestrator/scene01_orchestrator.py

from agent.schema.scene01.request import Scene01Request, ChatTurn
from agent.core.llm_client import LLMClient
from agent.core.retriever_client import RetrieverClient
from agent.schema.scene01.response import Scene01Response, GeneratedMessage
from typing import List
import logging

logger = logging.getLogger(__name__)

class Scene01Orchestrator:
    def __init__(self):
        self.llm_client = LLMClient()
        self.retriever_client = RetrieverClient()

    async def run(self, request: Scene01Request) -> Scene01Response:
        # 1. 히스토리 정리 (최근 3개 문답 그대로 사용)
        history_blocks = self._format_history(request.history)

        # 2. 기획안 요약 (선택)
        file_summary = await self._summarize_uploaded_file(request.file_url) if request.file_url else ""

        # 3. 프롬프트 결합
        final_prompt = self._compose_final_prompt(
            history_blocks,
            request.prompt,
            request.life_stage,
            file_summary
        )

        # 4. RAG 수행
        rag_augmented_knowledge = await self._retrieve_knowledge_with_rag(
            message_type=request.message_type.value,
            life_stage=request.life_stage,
            channels=[c.value for c in request.channels],
            query=final_prompt
        )

        # 5. 채널별 메시지 생성
        generated_messages: List[GeneratedMessage] = []
        for channel in request.channels:
            prompt_per_channel = self._build_prompt_per_channel(
                base_prompt=final_prompt,
                rag_knowledge=rag_augmented_knowledge,
                channel=channel.value
            )
            response_text = await self.llm_client.generate(
                llm_id=999,  # 🧠 LLM ID는 config로 분리 가능
                messages=[prompt_per_channel],
                llm_config={"temperature": 0.7, "maxTokens": 512}
            )
            generated_messages.append(GeneratedMessage(channel=channel.value, content=response_text.strip()))

        # 6. 하나의 문자열로 합쳐 응답
        result = "\n".join([f"{m.channel}: {m.content}" for m in generated_messages])

        return Scene01Response(
            result=result,
            used_prompt=final_prompt
        )

    # ========================= 내부 함수 정의 =========================

    def _format_history(self, history: List[ChatTurn]) -> str:
        if not history:
            return ""
        return "\n".join(
            [f"User: {turn.user}\nAI: {turn.ai}" for turn in history]
        )

    async def _summarize_uploaded_file(self, file_url: str) -> str:
        # TODO: PDF, DOCX, PPTX 요약 로직 구현 예정 (LangChain Document Loader 가능)
        logger.info(f"Summarizing uploaded file: {file_url}")
        return f"[기획안 요약]: (요약된 내용이 여기에 들어갑니다)"

    def _compose_final_prompt(self, history: str, user_prompt: str, life_stage: str, file_summary: str) -> str:
        return f"""[히스토리]
{history}

[라이프스테이지]
{life_stage} 대상 고객에게 적합한 문구를 작성해야 합니다.

[사용자 요청]
{user_prompt}

{file_summary}
"""

    async def _retrieve_knowledge_with_rag(self, message_type: str, life_stage: str, channels: List[str], query: str) -> str:
        # message_type에 따라 서로 다른 RAG Agent ID 사용 가능
        agent_id = self._select_agent_id_by_message_type(message_type)
        rag_response = await self.retriever_client.retrieve_and_generate(
            agent_id=agent_id,
            query=query,
            llm_config={"temperature": 0.3, "maxTokens": 512}
        )
        return rag_response.strip()

    def _select_agent_id_by_message_type(self, message_type: str) -> int:
        # TODO: 실제 Agent ID 매핑 테이블 연동
        mapping = {
            "대고객메시지": 101,
            "광고심의문구": 202,
            "유의문구": 203
        }
        return mapping.get(message_type, 101)

    def _build_prompt_per_channel(self, base_prompt: str, rag_knowledge: str, channel: str) -> str:
        return f"""{base_prompt}

[추가 정보 (RAG 기반)]:
{rag_knowledge}

[출력조건]
이 채널({channel})에 적합한 길이로 마케팅 메시지를 생성해주세요.
"""
