import psycopg2
from psycopg2 import Error

class Connector:
  def __init__(self, connection=None, cursor=None, user=None, password=None, host=None, port=None, database=None):
    try:
      self.connection = psycopg2.connect(user="root",
                                        password="1234",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="openweather_api")
      self.cursor = self.connection.cursor()
    except (Exception, Error) as error:
      print("Error with PostgreSQL", error)
