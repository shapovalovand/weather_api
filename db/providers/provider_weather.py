import datetime
from psycopg2 import Error
import json

class Crud_api:

  def __init__(self, connector, query=None):
    self.connection = connector.connection
    self.cursor = connector.cursor
    self.query = query

  def execute_query(self, query):
    self.cursor.execute(query)
    self.connection.commit()

  def create_entity(self):
    self.query = '''CREATE TABLE WEATHER
                            (ID SERIAL PRIMARY KEY    NOT NULL,
                            CITY_NAME       VARCHAR   NOT NULL,
                            DATE_TIME       TIMESTAMP NOT NULL,
                            DATA_JSON       TEXT      NOT NULL
                            );'''
    try:
      self.execute_query(self.query)
    except (Exception, Error) as error:
      print("Error with PostgreSQL", error)

  def get_all_table(self):
    try:
      self.cursor.execute("""SELECT table_name FROM information_schema.tables
                            WHERE table_schema NOT IN ('information_schema','pg_catalog')
                            ;""")
      return self.cursor.fetchall()
    except (Exception, Error) as error:
      print("Error with PostgreSQL", error)

  def get_weather_by_time(self, day, res_hour, city_name):
    date = datetime.timedelta(days=day)
    datenow = datetime.datetime.today() + date
    datenow = datenow.replace(hour=int(res_hour))
    try:
      self.cursor.execute(f'''SELECT DATA_JSON
                          FROM WEATHER
                          WHERE DATE_TIME = DATE_TRUNC('hour', TIMESTAMP '{datenow}')
                          AND CITY_NAME='{city_name}'
                          ;''')
      data = self.cursor.fetchall()
      return data
    except (Exception, Error) as error:
      print("Error with PostgreSQL", error)

  def parse_weather_and_insert(self, json_file):
    data_weather = json_file['list']
    city_name = json_file['city']['name']
    for weather in data_weather:
      date = datetime.datetime.fromtimestamp(weather['dt'])
      self.query = f"""INSERT INTO WEATHER (CITY_NAME, DATE_TIME, DATA_JSON) 
                       VALUES ('{city_name}', '{date}', '{json.dumps(weather)}');
                      """
      self.execute_query(self.query)
