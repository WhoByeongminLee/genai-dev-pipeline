from fastapi import FastAPI
from agent.api.v1 import scene01_endpoints, scene02_endpoints

app = FastAPI(
    title="GenAI Knowledge Agent",
    version="1.0.0"
)

app.include_router(scene01_endpoints.router, prefix="/v1")
app.include_router(scene02_endpoints.router, prefix="/v1")

@app.get("/")
def root():
    return {"message": "GenAI Agent is running 🚀"}
