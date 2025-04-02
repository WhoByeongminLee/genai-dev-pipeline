from pydantic import BaseModel

class ArticleResponse(BaseModel):
    title: str
    topic: str
    article_draft: str
