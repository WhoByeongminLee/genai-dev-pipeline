from fastapi import APIRouter, Depends
from agent.schema.scene02.request import ArticleRequest
from agent.schema.scene02.response import ArticleResponse
from agent.orchestrator.scene02_orchestrator import ArticleOrchestrator

router = APIRouter()

def get_orchestrator():
    return ArticleOrchestrator()

@router.post("/scene02/article-draft", response_model=ArticleResponse)
async def generate_article(
    request: ArticleRequest,
    orchestrator: ArticleOrchestrator = Depends(get_orchestrator)
):
    return await orchestrator.generate_article(request)
