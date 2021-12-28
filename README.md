# OpenWeather_API 

It is necessary to implement a service that implements receiving
weather data API.

## Stack: 
* python
* aiohttp
* psycopg2
* docker-compose

## First start

1. Run container with DB: docker-compose up
2. Down container: docker-compose down -v
3. Run server: python3 app.py
4. Endpoint format: http://localhost:3000/weather?country_code=RU&city=Moscow&date=<3>T12:00

## Improvements for my app

* add environment variables
* decomposition for app module
* add testing