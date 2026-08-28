import utils


def test_compute_estimated_gdp():
    population = 1000000
    exchange_rate = 2

    result = utils.compute_estimated_gdp(population, exchange_rate)

    assert result is not None
    assert result > 0


def test_compute_estimated_gdp_with_none_population():
    result = utils.compute_estimated_gdp(None, 2)

    assert result is None


def test_compute_estimated_gdp_with_zero_exchange_rate():
    result = utils.compute_estimated_gdp(1000000, 0)

    assert result is None