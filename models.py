from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.sql import expression
from sqlalchemy.sql.schema import Sequence
from database import Base
from sqlalchemy import Boolean, Text

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    capital = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    population = Column(Integer, nullable=False)
    currency_code = Column(String(10), nullable=True)
    exchange_rate = Column(Float, nullable=True)
    estimated_gdp = Column(Float, nullable=True)
    flag_url = Column(String(1024), nullable=True)
    last_refreshed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

