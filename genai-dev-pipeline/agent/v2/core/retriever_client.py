#POST /openapi/agent-chat/v1/agent-messages (isRagOn=True)

import httpx
from agent.config.settings import settings

class RetrieverClient:
    def __init__(self):
        self.headers = {
            "x-openapi-token": settings.OPENAPI_TOKEN,
            "x-generative-ai-client": settings.GENERATIVE_AI_CLIENT,
            "x-generative-ai-user-email": settings.GENERATIVE_AI_USER_EMAIL,
            "Content-Type": "application/json"
        }
        self.endpoint = f"{settings.BASE_URL}/dev/kbcommon/agentv1/1/openapi/agent-chat/v1/agent-messages"

    async def retrieve_and_generate(self, agent_id: int, query: str, llm_config: dict) -> str:
        body = {
            "agentId": agent_id,
            "contents": [query],
            "isStream": False,
            "isRagOn": True,
            "llmConfig": llm_config
        }

        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(self.endpoint, headers=self.headers, json=body)
            response.raise_for_status()
            data = response.json()
            return data.get("content")
