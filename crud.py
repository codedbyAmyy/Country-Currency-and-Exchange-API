from sqlalchemy import select, update, delete
from models import Country
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

async def get_country_by_name(session: AsyncSession, name: str):
    q = select(Country).where(Country.name.ilike(name))
    res = await session.execute(q)
    return res.scalars().first()

async def list_countries(session: AsyncSession, region=None, currency=None, sort=None):
    q = select(Country)
    if region:
        q = q.where(Country.region == region)
    if currency:
        q = q.where(Country.currency_code == currency)
    if sort:
        if sort == "gdp_desc":
            q = q.order_by(Country.estimated_gdp.desc())
        elif sort == "gdp_asc":
            q = q.order_by(Country.estimated_gdp.asc())
        elif sort == "name_asc":
            q = q.order_by(Country.name.asc())
    res = await session.execute(q)
    return res.scalars().all()

async def upsert_country(session: AsyncSession, payload: dict, auto_commit: bool = True):
    existing = await get_country_by_name(session, payload["name"])
    if existing:
        for k, v in payload.items():
            setattr(existing, k, v)
        existing.last_refreshed_at = datetime.now(timezone.utc)
        session.add(existing)
        
        if auto_commit:
            await session.commit()
            await session.refresh(existing)
        return existing, False
    else:
        obj = Country(**payload)
        obj.last_refreshed_at = datetime.now(timezone.utc)
        session.add(obj)
        
        if auto_commit:
            await session.commit()
            await session.refresh(obj)
        return obj, True
    
async def bulk_upsert_countries(session: AsyncSession, payloads: list[dict]):
    # 1. Fetch all existing countries in ONE single query
    q = select(Country)
    res = await session.execute(q)
    existing_map = {c.name.lower(): c for c in res.scalars().all()}
    
    # 2. Process all payloads in memory
    for payload in payloads:
        name_key = payload["name"].lower()
        if name_key in existing_map:
            existing = existing_map[name_key]
            for k, v in payload.items():
                setattr(existing, k, v)
            existing.last_refreshed_at = datetime.now(timezone.utc)
        else:
            obj = Country(**payload)
            obj.last_refreshed_at = datetime.now(timezone.utc)
            session.add(obj)
            
    # 3. Fire the massive write transaction
    await session.commit()

async def delete_country(session: AsyncSession, name: str):
    existing = await get_country_by_name(session, name)
    if not existing:
        return False
    await session.delete(existing)
    await session.commit()
    return True

async def get_status(session: AsyncSession):
    q = select(Country)
    res = await session.execute(q)
    countries = res.scalars().all()
    total = len(countries)
    last_ts = None
    if countries:
        last_ts = max([c.last_refreshed_at for c in countries if c.last_refreshed_at])
    return total, last_ts
