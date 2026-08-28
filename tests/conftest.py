import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import ASGITransport, AsyncClient

from database import Base, get_session
from main import app
from models import Country


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture
async def test_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def sample_countries(test_session):
    countries = [
        Country(
            name="Nigeria",
            capital="Abuja",
            region="Africa",
            population=223804632,
            currency_code="NGN",
            exchange_rate=1500.0,
            estimated_gdp=149203088000.0,
            flag_url="https://flagcdn.com/ng.svg",
        ),
        Country(
            name="United States",
            capital="Washington, D.C.",
            region="Americas",
            population=331000000,
            currency_code="USD",
            exchange_rate=1.0,
            estimated_gdp=496500000000.0,
            flag_url="https://flagcdn.com/us.svg",
        ),
        Country(
            name="Ghana",
            capital="Accra",
            region="Africa",
            population=31072940,
            currency_code="GHS",
            exchange_rate=12.5,
            estimated_gdp=3728752800.0,
            flag_url="https://flagcdn.com/gh.svg",
        ),
    ]

    test_session.add_all(countries)
    await test_session.commit()

    return countries


@pytest.fixture
async def client(test_session):
    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()