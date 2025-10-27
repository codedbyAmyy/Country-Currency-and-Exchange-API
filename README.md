# Country Currency & Exchange API

## Overview

The Country Currency & Exchange API is a powerful tool for developers looking to integrate comprehensive and up-to-date country and currency information into their applications. It provides access to a wide range of data, from basic country details to the latest currency exchange rates, all through a simple and intuitive RESTful API.

Whether you're building a travel app, a financial tool, or an e-commerce platform, this API makes it easy to fetch the data you need to create a seamless user experience.

## Key Features

- **Extensive Country Data**: Retrieve detailed information for over 250 countries, including capital, region, population, and flag URL.
- **Real-Time Exchange Rates**: Get the latest exchange rates with the US Dollar as the base currency, ensuring your financial calculations are always accurate.
- **Automated Data Refresh**: A dedicated endpoint allows you to refresh the entire dataset, ensuring your application is always working with the most current information.
- **Dynamic Summary Image**: Generate and serve a summary image that visualizes the top 5 countries by estimated GDP, perfect for dashboards and reports.
- **Flexible Filtering and Sorting**: Easily filter countries by region or currency, and sort the results by name or estimated GDP to quickly find the data you need.
- **Seamless Integration**: Built with FastAPI, the API offers automatic interactive documentation, making it easy to explore and test the available endpoints.

## Getting Started

### Prerequisites

- Python 3.8+
- An active internet connection

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following variables. **Note**: Before running the application, make sure you have created the `countries_db` database in your MySQL instance.
   ```env
   DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/countries_db # Replace with your database credentials
   PORT=8000
   REFRESH_TIMEOUT=30
   CACHE_IMAGE_PATH=cache/summary.png
   BASE_CURRENCY=USD
   RESTCURRENCIES_URL=https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
   EXCHANGE_RATES_URL=https://open.er-api.com/v6/latest/USD
   ```

### Running the Application

- **Run the API**:
  ```bash
  uvicorn main:app --reload
  ```
- **Access the documentation**:
  Once the server is running, you can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## API Documentation

The following is a detailed description of the available API endpoints. For a complete interactive experience, you can also access the Swagger UI documentation at `http://127.0.0.1:8000/docs`.

### Refresh Country Data

- **Endpoint**: `POST /countries/refresh`
- **Description**: Triggers a refresh of the country and currency data from the external APIs. This operation can take a few moments to complete, as it fetches and processes a large amount of data.
- **Successful Response**:
  ```json
  {
    "message": "Refresh successful",
    "total_countries": 250,
    "last_refreshed_at": "2023-10-27T10:00:00Z"
  }
  ```

### Get All Countries

- **Endpoint**: `GET /countries`
- **Description**: Retrieves a list of all countries in the database. You can use query parameters to filter and sort the results.
- **Query Parameters**:
  - `region` (optional): Filter by a specific region (e.g., "Africa").
  - `currency` (optional): Filter by a specific currency code (e.g., "USD").
  - `sort` (optional): Sort the results. Options are `gdp_desc`, `gdp_asc`, or `name_asc`.
- **Example Request**: `GET /countries?region=Europe&sort=gdp_desc`
- **Successful Response**:
  ```json
  [
    {
      "name": "Country Name",
      "capital": "Capital City",
      "region": "Europe",
      "population": 12345678,
      "currency_code": "EUR",
      "exchange_rate": 1.1,
      "estimated_gdp": 1234567890.12,
      "flag_url": "https://example.com/flag.svg"
    }
  ]
  ```

### Get API Status

- **Endpoint**: `GET /status`
- **Description**: Returns the total number of countries in the database and the timestamp of the last successful data refresh.
- **Successful Response**:
  ```json
  {
    "total_countries": 250,
    "last_refreshed_at": "2023-10-27T10:00:00Z"
  }
  ```

### Get Summary Image

- **Endpoint**: `GET /countries/image`
- **Description**: Returns a PNG image summarizing the top 5 countries by estimated GDP. This is useful for dashboards or reports.
- **Successful Response**: A PNG image file.

### Get a Specific Country

- **Endpoint**: `GET /countries/{name}`
- **Description**: Retrieves detailed information for a single country, specified by its name. The name is case-insensitive.
- **Example Request**: `GET /countries/United%20States`
- **Successful Response**:
  ```json
  {
    "name": "United States",
    "capital": "Washington, D.C.",
    "region": "Americas",
    "population": 331002651,
    "currency_code": "USD",
    "exchange_rate": 1,
    "estimated_gdp": 331002651,
    "flag_url": "https://restcountries.com/data/usa.svg"
  }
  ```

### Delete a Country

- **Endpoint**: `DELETE /countries/{name}`
- **Description**: Deletes a country from the database. The name is case-insensitive.
- **Successful Response**:
  ```json
  {
    "message": "Deleted"
  }
  ```

## Data Sources

- **Countries Data**: [restcountries.com](https://restcountries.com)
- **Exchange Rates**: [exchangerate-api.com](https://www.exchangerate-api.com)

## Tech Stack

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapper (ORM) for Python.
- **AioMySQL**: An async library for accessing a MySQL database.
- **Uvicorn**: An ASGI server for running FastAPI applications.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or feedback, please feel free to reach out.

- **Author**: Your Name
- **Email**: your.email@example.com
