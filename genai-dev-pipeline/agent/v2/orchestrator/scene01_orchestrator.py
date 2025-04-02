import yaml
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agent.core.llm_client import LLMClient
from agent.schema.scene01.request import MarketingRequest
from agent.schema.scene01.response import MarketingResponse

class MarketingOrchestrator:
    def __init__(self):
        # YAML Prompt 로드
        prompt_path = Path(__file__).parent.parent / "prompts" / "scene01_prompt.yaml"
        with open(prompt_path, "r") as f:
            prompt_config = yaml.safe_load(f)

        self.prompt = PromptTemplate(
            input_variables=prompt_config["input_variables"],
            template=prompt_config["template"]
        )
        self.llm_client = LLMClient()

    async def generate_marketing_copy(self, request: MarketingRequest) -> MarketingResponse:
        # LangChain Chain 실행
        chain = LLMChain(llm=self.llm_client, prompt=self.prompt)
        result = await chain.arun(product=request.product, concept=request.concept)

        return MarketingResponse(
            product=request.product,
            concept=request.concept,
            marketing_copy=result
        )
