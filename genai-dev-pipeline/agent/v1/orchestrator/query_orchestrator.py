from agent.core.llm_client import LLMClient
from agent.core.retriever_client import RetrieverClient
from agent.schema.query import QueryRequest
from agent.schema.response import QueryResponse, RetrievedDocument

class QueryOrchestrator:
    def __init__(self):
        self.retriever_client = RetrieverClient()
        self.llm_client = LLMClient()

    async def handle_query(self, request: QueryRequest) -> QueryResponse:
        retrieved_docs = await self.retriever_client.retrieve(request.query)
        retrieved_documents = [
            RetrievedDocument(id=doc["id"], content=doc["content"]) 
            for doc in retrieved_docs
        ]

        context = "\n".join([doc.content for doc in retrieved_documents])
        prompt = f"Context:\n{context}\n\nQuestion:\n{request.query}\n\nAnswer:"

        generated_answer = await self.llm_client.generate(prompt)

        return QueryResponse(
            query=request.query,
            retrieved_documents=retrieved_documents,
            generated_answer=generated_answer
        )
