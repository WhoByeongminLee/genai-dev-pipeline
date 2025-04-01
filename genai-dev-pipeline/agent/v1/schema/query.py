from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., example="What is Clean Architecture?")
