from fastapi import FastAPI
from agent.api.v1 import endpoints

app = FastAPI(
    title="Knowledge Agent API",
    description="Retrieval + LLM 기반 지식 응답 서비스",
    version="1.0.0"
)

app.include_router(endpoints.router, prefix="/v1")

@app.get("/")
def read_root():
    return {"message": "Knowledge Agent is running 🚀"}
