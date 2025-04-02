from pydantic import BaseModel

class MarketingResponse(BaseModel):
    product: str
    concept: str
    marketing_copy: str
