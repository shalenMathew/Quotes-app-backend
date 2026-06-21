from pydantic import BaseModel, ConfigDict


class QuoteResponse(BaseModel):
    q: str
    a: str

    model_config = ConfigDict(from_attributes=True)