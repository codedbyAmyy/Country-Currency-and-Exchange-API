from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CountryBase(BaseModel):
    name: str = Field(..., min_length=1)
    capital: Optional[str]
    region: Optional[str]
    population: int = Field(..., ge=0)
    currency_code: Optional[str]
    exchange_rate: Optional[float]
    estimated_gdp: Optional[float]
    flag_url: Optional[str]
    last_refreshed_at: Optional[datetime]

class CountryResponse(CountryBase):
    id: int

    class Config:
        from_attributes = True

class StatusResponse(BaseModel):
    total_countries: int
    last_refreshed_at: Optional[datetime]
