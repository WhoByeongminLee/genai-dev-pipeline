from pydantic import BaseModel, Field

class ArticleRequest(BaseModel):
    title: str = Field(..., example="The Future of AI Agents")
    topic: str = Field(..., example="How AI agents are changing the business world")
