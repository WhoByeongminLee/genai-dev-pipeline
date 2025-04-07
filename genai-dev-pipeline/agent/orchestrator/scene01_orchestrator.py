# agent/orchestrator/scene01_orchestrator.py

from agent.schema.scene01.request import Scene01Request, ChatTurn
from agent.core.llm_client import LLMClient
from agent.core.retriever_client import RetrieverClient
from agent.schema.scene01.response import Scene01Response, GeneratedMessage
from typing import List
from langchain.prompts import PromptTemplate
import yaml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Scene01Orchestrator:
    def __init__(self):
        self.llm_client = LLMClient()
        self.retriever_client = RetrieverClient()
        self.prompt_config = self._load_prompt_yaml(scene="scene01", version="v1", name="base_prompt.yaml")
        self.agent_id_map = self._load_agent_id_mapping(scene="scene01")

    def _load_agent_id_mapping(self, scene: str) -> dict:
        path = Path(f"agent/config/agent_id_mapping.yaml")
        with open(path, "r", encoding="utf-8") as f:
            full_map = yaml.safe_load(f)
        return full_map.get(scene, {})
    
    async def run(self, request: Scene01Request) -> Scene01Response:
        # 1. 히스토리 문자열 포맷 구성
        history_block = self._format_history(request.history)

        # 2. 기획안 요약 (선택 사항)
        file_summary = await self._summarize_uploaded_file(request.file_url) if request.file_url else ""

        # 3. 프롬프트 템플릿 구성 (LangChain PromptTemplate 활용)
        base_prompt = self._build_base_prompt(
            history=history_block,
            user_prompt=request.prompt,
            life_stage=request.life_stage,
            file_summary=file_summary,
            channels=[c.value for c in request.channels]
        )

        # 4. RAG 기반 강화 프롬프트 호출
        rag_knowledge = await self._retrieve_knowledge_with_rag(
            message_type=request.message_type.value,
            life_stage=request.life_stage,
            channels=[c.value for c in request.channels],
            query=base_prompt
        )

        # 5. 채널별 메시지 생성
        generated_messages: List[GeneratedMessage] = []
        for channel in request.channels:
            full_prompt = self._build_channel_prompt(
                base_prompt=base_prompt,
                rag_knowledge=rag_knowledge,
                channel=channel.value
            )
            response_text = await self.llm_client.generate(
                llm_id=999,
                messages=[full_prompt],
                llm_config={"temperature": 0.7, "maxTokens": 512}
            )
            generated_messages.append(GeneratedMessage(channel=channel.value, content=response_text.strip()))

        # 6. 응답 문자열 구성
        result = "\n\n".join([f"[{m.channel}]\n{m.content}" for m in generated_messages])
        # result = "\n".join([f"{m.channel}: {m.content}" for m in generated_messages])

        return Scene01Response(
            result=result,
            used_prompt=base_prompt  # 최초 prompt만 기록 (채널별 개별 프롬프트는 생략)
        )

    # =============== 내부 헬퍼 메서드 ===================

    def _format_history(self, history: List[ChatTurn]) -> str:
        if not history:
            return ""
        return "\n".join([f"User: {turn.user}\nAI: {turn.ai}" for turn in history])
    
    async def _summarize_uploaded_file(self, file_url: str) -> str:
        logger.info(f"Summarizing uploaded file: {file_url}")
        return f"[기획안 요약]: {file_url}(요약된 내용이 여기에 들어갑니다)"  # TODO: LangChain 기반으로 확장 예정

    async def _retrieve_knowledge_with_rag(self, message_type: str, life_stage: str, channels: List[str], query: str) -> str:
        agent_id = self._select_agent_id_by_message_type(message_type)
        rag_response = await self.retriever_client.retrieve_and_generate(
            agent_id=agent_id,
            query=query,
            llm_config={"temperature": 0.3, "maxTokens": 512}
        )
        return rag_response.strip()

    def _select_agent_id_by_message_type(self, message_type: str) -> int:
        return self.agent_id_map.get(message_type, 0)  # 기본값 0 또는 예외 처리

    def _build_base_prompt(self, history: str, user_prompt: str, life_stage: str, file_summary: str, channels: List[str]) -> str:
        template = PromptTemplate.from_template(self.prompt_config["user_prompt_template"])
        return template.format(
            history=history,
            user_prompt=user_prompt,
            life_stage=life_stage,
            file_summary=file_summary,
            channel=", ".join(channels),
            rag_knowledge=""
        )

    def _build_channel_prompt(self, base_prompt: str, rag_knowledge: str, channel: str) -> str:
        template = PromptTemplate.from_template(self.prompt_config["channel_instruction_template"])
        channel_part = template.format(rag_knowledge=rag_knowledge, channel=channel)
        return f"{base_prompt}\n\n{channel_part}"

    def _load_prompt_yaml(self, scene: str, version: str, name: str) -> dict:
        path = Path(__file__).parent.parent / "prompts" / scene / version / name
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
        """
        path = Path(f"prompts/{scene}/{version}/{name}")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
        """
