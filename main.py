from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, engine, Base
import crud, utils
from schema import CountryResponse, StatusResponse
from dotenv import load_dotenv
import os
from typing import List, Optional
from datetime import datetime, timezone

load_dotenv()
CACHE_IMAGE_PATH = os.getenv("CACHE_IMAGE_PATH", "cache/summary.png")

app = FastAPI(title="Country Currency & Exchange API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def error_400(details: dict):
    return JSONResponse(status_code=400, content={"error": "Validation failed", "details": details})

@app.post("/countries/refresh")
async def refresh_countries(session: AsyncSession = Depends(get_session)):
    try:
        countries_data = utils.fetch_countries()
    except Exception as e:
        return JSONResponse(status_code=503, content={"error": "External data source unavailable", "details": "Could not fetch data from Countries API"})

    try:
        rates = utils.fetch_exchange_rates()
    except Exception as e:
        return JSONResponse(status_code=503, content={"error": "External data source unavailable", "details": "Could not fetch data from Exchange Rates API"})

    processed = []
    for c in countries_data:
        name = c.get("name")
        if not name:
            continue  
        capital = c.get("capital")
        region = c.get("region")
        population = c.get("population") if isinstance(c.get("population"), (int, float)) else 0
        currencies = c.get("currencies") or []
        flag = c.get("flag") or c.get("flags", {}).get("svg")
        currency_code = None
        exchange_rate = None
        estimated_gdp = None

        if isinstance(currencies, list) and len(currencies) > 0:
            first = currencies[0]
            if isinstance(first, dict):
                currency_code = first.get("code")
            elif isinstance(first, str):
                currency_code = first
            if currency_code:
                exchange_rate = rates.get(currency_code)
                if exchange_rate is not None:
                    try:
                        estimated_gdp = utils.compute_estimated_gdp(population, exchange_rate)
                    except Exception:
                        estimated_gdp = None
                else:
                    exchange_rate = None
                    estimated_gdp = None
        else:
            currency_code = None
            exchange_rate = None
            estimated_gdp = 0

        payload = {
            "name": name.strip(),
            "capital": capital,
            "region": region,
            "population": population or 0,
            "currency_code": currency_code,
            "exchange_rate": exchange_rate,
            "estimated_gdp": estimated_gdp,
            "flag_url": flag
        }
        processed.append(payload)

    from datetime import datetime
    last_refreshed = datetime.now(timezone.utc)
    for payload in processed:
        if payload.get("currency_code") and payload.get("exchange_rate"):
            payload["estimated_gdp"] = utils.compute_estimated_gdp(payload["population"], payload["exchange_rate"])
        elif payload.get("currency_code") is None and payload.get("exchange_rate") is None:
            payload["estimated_gdp"] = 0
        await crud.upsert_country(session, payload)

    total, _ = await crud.get_status(session)
    all_countries = await crud.list_countries(session)
    top5 = sorted([{
        "name": c.name,
        "estimated_gdp": c.estimated_gdp or 0
    } for c in all_countries], key=lambda x: x["estimated_gdp"] or 0, reverse=True)[:5]

    utils.generate_summary_image(total, top5, last_refreshed.isoformat(), out_path=CACHE_IMAGE_PATH)

    return {"message": "Refresh successful", "total_countries": total, "last_refreshed_at": last_refreshed.isoformat()}

@app.get("/countries", response_model=List[CountryResponse])
async def get_countries(region: Optional[str] = None, currency: Optional[str] = None, sort: Optional[str] = None, session: AsyncSession = Depends(get_session)):
    countries = await crud.list_countries(session, region=region, currency=currency, sort=sort)
    return countries

@app.get("/status", response_model=StatusResponse)
async def status(session: AsyncSession = Depends(get_session)):
    total, last_ts = await crud.get_status(session)
    return {"total_countries": total, "last_refreshed_at": last_ts}

@app.get("/countries/image")
async def get_image():
    if not os.path.exists(CACHE_IMAGE_PATH):
        return JSONResponse(status_code=404, content={"error": "Summary image not found"})
    return FileResponse(CACHE_IMAGE_PATH, media_type="image/png")


@app.get("/countries/{name}", response_model=CountryResponse)
async def get_country(name: str, session: AsyncSession = Depends(get_session)):
    country = await crud.get_country_by_name(session, name)
    if not country:
        return JSONResponse(status_code=404, content={"error": "Country not found"})
    return country

@app.delete("/countries/{name}")
async def delete_country(name: str, session: AsyncSession = Depends(get_session)):
    ok = await crud.delete_country(session, name)
    if not ok:
        return JSONResponse(status_code=404, content={"error": "Country not found"})
    return {"message": "Deleted"}

