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
   Create a `.env` file in the root directory and add the following variables:
   ```env
   DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/countries_db
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

### Endpoints

- **`POST /countries/refresh`**: Refreshes the country and currency data from external APIs.
- **`GET /countries`**: Retrieves a list of all countries.
- **`GET /status`**: Returns the total number of countries and the last refresh timestamp.
- **`GET /countries/image`**: Returns a summary image of the top 5 countries by GDP.
- **`GET /countries/{name}`**: Retrieves detailed information for a specific country.
- **`DELETE /countries/{name}`**: Deletes a country from the database.

## Data Sources

- **Countries Data**: [restcountries.com](https://restcountries.com)
- **Exchange Rates**: [exchangerate-api.com](https://www.exchangerate-api.com)

## Tech Stack

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapper (ORM) for Python.
- **AioMySQL**: An async library for accessing a MySQL database.
- **Uvicorn**: An ASGI server for running FastAPI applications.
