import yaml
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agent.core.llm_client import LLMClient
from agent.schema.scene02.request import ArticleRequest
from agent.schema.scene02.response import ArticleResponse

class ArticleOrchestrator:
    def __init__(self):
        # YAML Prompt 로드
        prompt_path = Path(__file__).parent.parent / "prompts" / "scene02_prompt.yaml"
        with open(prompt_path, "r") as f:
            prompt_config = yaml.safe_load(f)

        self.prompt = PromptTemplate(
            input_variables=prompt_config["input_variables"],
            template=prompt_config["template"]
        )
        self.llm_client = LLMClient()

    async def generate_article(self, request: ArticleRequest) -> ArticleResponse:
        chain = LLMChain(llm=self.llm_client, prompt=self.prompt)
        result = await chain.arun(title=request.title, topic=request.topic)

        return ArticleResponse(
            title=request.title,
            topic=request.topic,
            article_draft=result
        )
