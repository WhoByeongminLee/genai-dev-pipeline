import httpx
from agent.config.settings import settings

class RetrieverClient:
    def __init__(self):
        self.base_url = settings.RETRIEVER_API_BASE_URL
        self.headers = {"Authorization": f"Bearer {settings.RETRIEVER_API_KEY}"}

    async def retrieve(self, query: str) -> list:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/retrieve",
                headers=self.headers,
                json={"query": query}
            )
            response.raise_for_status()
            return response.json()["documents"]
