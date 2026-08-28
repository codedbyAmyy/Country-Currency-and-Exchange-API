import pytest


@pytest.mark.anyio
async def test_status(client):
    response = await client.get("/status")

    assert response.status_code == 200

    data = response.json()

    assert data["total_countries"] == 0
    assert data["last_refreshed_at"] is None


@pytest.mark.anyio
async def test_get_countries(client, sample_countries):
    response = await client.get("/countries")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3
    assert isinstance(data, list)


@pytest.mark.anyio
async def test_get_country(client, sample_countries):
    response = await client.get("/countries/Nigeria")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Nigeria"
    assert data["capital"] == "Abuja"
    assert data["region"] == "Africa"
    assert data["currency_code"] == "NGN"


@pytest.mark.anyio
async def test_get_nonexistent_country(client, sample_countries):
    response = await client.get("/countries/Canada")

    assert response.status_code == 404

    data = response.json()

    assert data["error"] == "Country not found"
    
@pytest.mark.anyio
async def test_filter_countries_by_region(client, sample_countries):
    response = await client.get("/countries?region=Africa")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(country["region"] == "Africa" for country in data)
    
@pytest.mark.anyio
async def test_filter_countries_by_currency(client, sample_countries):
    response = await client.get("/countries?currency=NGN")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Nigeria"
    
@pytest.mark.anyio
async def test_sort_countries_by_gdp_desc(client, sample_countries):
    response = await client.get("/countries?sort=gdp_desc")

    assert response.status_code == 200

    data = response.json()

    gdps = [country["estimated_gdp"] for country in data]

    assert gdps == sorted(gdps, reverse=True)
    
@pytest.mark.anyio
async def test_sort_countries_by_name(client, sample_countries):
    response = await client.get("/countries?sort=name_asc")

    assert response.status_code == 200

    data = response.json()

    names = [country["name"] for country in data]

    assert names == sorted(names)
    
