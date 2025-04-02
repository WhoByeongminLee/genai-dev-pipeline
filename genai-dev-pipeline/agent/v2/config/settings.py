from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAPI_TOKEN: str
    GENERATIVE_AI_CLIENT: str
    GENERATIVE_AI_USER_EMAIL: str
    BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
