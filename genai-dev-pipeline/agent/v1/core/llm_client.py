import httpx
from agent.config.settings import settings

class LLMClient:
    def __init__(self):
        self.base_url = settings.LLM_API_BASE_URL
        self.headers = {"Authorization": f"Bearer {settings.LLM_API_KEY}"}

    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/generate",
                headers=self.headers,
                json={"prompt": prompt}
            )
            response.raise_for_status()
            return response.json()["result"]
