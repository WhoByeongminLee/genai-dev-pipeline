from pydantic import BaseModel, Field

class MarketingRequest(BaseModel):
    product: str = Field(..., example="Eco-friendly Water Bottle")
    concept: str = Field(..., example="Sustainability and Minimalism")
