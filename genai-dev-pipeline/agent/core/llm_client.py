# agent/core/llm_client.py
#POST /openapi/chat/v1/messages (isRagOn=False)

import httpx
from agent.config.settings import settings

class LLMClient:
    def __init__(self):
        self.headers = {
            "x-openapi-token": settings.OPENAPI_TOKEN,
            "x-generative-ai-client": settings.GENERATIVE_AI_CLIENT,
            "x-generative-ai-user-email": settings.GENERATIVE_AI_USER_EMAIL,
            "Content-Type": "application/json"
        }
        self.endpoint = f"{settings.BASE_URL}/dev/kbcommon/agentv1/1/openapi/chat/v1/messages"

    async def generate(self, llm_id: int, messages: list[str], llm_config: dict) -> str:
        body = {
            "llmId": llm_id,
            "contents": messages,
            "isStream": False,
            "llmConfig": llm_config
        }

        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(self.endpoint, headers=self.headers, json=body)
            response.raise_for_status()
            data = response.json()
            return data.get("content")
