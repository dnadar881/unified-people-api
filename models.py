from pydantic import BaseModel

class SearchResponse(BaseModel):
    total: int
    credits_used: int
    results: list
