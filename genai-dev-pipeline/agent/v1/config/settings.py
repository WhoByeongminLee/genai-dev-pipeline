from pydantic import BaseSettings

class Settings(BaseSettings):
    LLM_API_BASE_URL: str
    LLM_API_KEY: str
    RETRIEVER_API_BASE_URL: str
    RETRIEVER_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
