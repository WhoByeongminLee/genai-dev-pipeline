from fastapi import APIRouter, Depends
from agent.schema.query import QueryRequest
from agent.schema.response import QueryResponse
from agent.orchestrator.query_orchestrator import QueryOrchestrator

router = APIRouter()

def get_orchestrator():
    return QueryOrchestrator()

@router.post("/query", response_model=QueryResponse)
async def query_knowledge(
    request: QueryRequest,
    orchestrator: QueryOrchestrator = Depends(get_orchestrator)
):
    return await orchestrator.handle_query(request)
