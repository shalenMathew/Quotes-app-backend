from pydantic import BaseModel, ConfigDict


class QuoteSchema(BaseModel):
    q: str
    a: str


class QuoteResponse(QuoteSchema):
    model_config = ConfigDict(from_attributes=True)