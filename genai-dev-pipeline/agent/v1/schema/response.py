from pydantic import BaseModel
from typing import List

class RetrievedDocument(BaseModel):
    id: str
    content: str

class QueryResponse(BaseModel):
    query: str
    retrieved_documents: List[RetrievedDocument]
    generated_answer: str
