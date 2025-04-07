import os

class Settings:
    OPENAPI_TOKEN: str = os.getenv("OPENAPI_TOKEN", "test-token")
    GENERATIVE_AI_CLIENT: str = os.getenv("GEN_AI_CLIENT", "mock-client")
    GENERATIVE_AI_USER_EMAIL: str = os.getenv("GEN_AI_EMAIL", "test@example.com")
    BASE_URL: str = os.getenv("BASE_URL", "https://mock-api")
    IS_MOCK_MODE: bool = os.getenv("IS_MOCK_MODE", "true").lower() == "true"

settings = Settings()