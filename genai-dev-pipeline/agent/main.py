# agent/main.py

from fastapi import FastAPI
from agent.api.router import api_router

app = FastAPI(
    title="GenAI Knowledge Agent",
    version="1.0.0"
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "GenAI Agent is running 🚀"}
