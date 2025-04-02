import yaml
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agent.core.llm_client import LLMClient
from agent.core.retriever_client import RetrieverClient
from agent.schema.scene01.request import MarketingRequest
from agent.schema.scene01.response import MarketingResponse

class MarketingOrchestrator:
    def __init__(self):
        # Prompt YAML 로드
        prompt_path = Path(__file__).parent.parent / "prompts" / "scene01_prompt.yaml"
        with open(prompt_path, "r") as f:
            prompt_config = yaml.safe_load(f)

        self.prompt = PromptTemplate(
            input_variables=prompt_config["input_variables"] + ["retrieved_info"],
            template=prompt_config["template"]
        )
        self.llm_client = LLMClient()
        self.retriever_client = RetrieverClient()

        # 기본 LLM Config
        self.llm_config = {
            "do_sample": True,
            "max_new_tokens": 512,
            "return_full_text": False,
            "seed": None,
            "top_k": 14,
            "top_p": 0.94,
            "temperature": 0.4,
            "repetition_penalty": 1.0
        }

    async def generate_marketing_copy(self, request: MarketingRequest) -> MarketingResponse:
        # 1. RAG 수행 (Retrieval + Generation)
        rag_info = await self.retriever_sclient.retrieve_and_generate(
            agent_id=9,  # 🔥 사용 중인 Agent ID로 교체 가능
            query=f"{request.product} {request.concept} 관련 정보 알려줘",
            llm_config=self.llm_config
        )

        # 2. LangChain Prompt 실행
        chain = LLMChain(llm=self.llm_client, prompt=self.prompt)
        result = await chain.arun(
            product=request.product,
            concept=request.concept,
            retrieved_info=rag_info
        )

        return MarketingResponse(
            product=request.product,
            concept=request.concept,
            marketing_copy=result
        )
