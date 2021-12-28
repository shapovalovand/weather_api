from aiohttp import web
import aiohttp
import asyncio
import requests
import json
from db.providers.provider_weather import Crud_api
from db.connector.connection_db import Connector

connect = Connector()
API = Crud_api(connect)

class Weather_request:

  def __init__(self, appid=None, city=None, day=None, time=None):
    self.appid = appid
    self.city = city
    self.day = day
    self.time = time

  async def get(self):
    params = {'q': f'{self.city}',
              'appid': f'{self.appid}'}
    URL = 'https://api.openweathermap.org/data/2.5/forecast?'
    async with aiohttp.ClientSession() as session:
      async with session.request('GET', URL, params=params) as response:
        resp = await response.json()
        API.parse_weather_and_insert(resp)

  async def hadndle_req(self):
    try:
      loop = asyncio.get_event_loop()
      task =  asyncio.create_task(await self.get())
      results = await loop.run_until_complete(asyncio.gather(*task))
      return results
    except Exception as e:
      print('Got an exception:', e)

  async def req_search_weather(self):
    try:
      data = API.get_weather_by_time(self.day, self.time, self.city)
      if len(data) == 0: 
        await self.hadndle_req()
        data = API.get_weather_by_time(self.day, self.time, self.city)
      return data

    except (Exception) as error:
      print("Error query: ", error)

async def handle(request):
  country_code = request.rel_url.query['country_code']
  city = request.rel_url.query['city']
  date = request.rel_url.query['date']
  time = int(date.split('>')[1].split('T')[1].split(':')[0])
  day = int(date.split('>')[0].split('<')[1])
  wether_req = Weather_request(appid='d1bf65db43371e6ce77368c4a9c7a5cf', city=city, day=day, time=time)
  return web.Response(text=str(await wether_req.req_search_weather()))

app = web.Application()
app.add_routes([web.get('/weather', handle)])

if __name__ == '__main__':
    try:
      connect.cursor.execute("SELECT version();")
      data = API.get_all_table()
      if len(data) == 0:
        API.create_entity()
      else:
        if data[0].count('weather') == 0: 
          API.create_entity()

      if connect.connection:
        web.run_app(app, port = 3000)

    except (Exception) as error:
        print("Error with PostgreSQL", error)
    finally:
        if connect.connection:
            connect.cursor.close()
            connect.connection.close()
            print("Connection with PostgreSQL close")
