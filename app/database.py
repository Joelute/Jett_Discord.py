
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os
load_dotenv()


class Database_connection():
  
  def __init__(self):
    self.conn = self.try_connection()

  def try_connection(self):
    while True:
      try:
        conn = psycopg2.connect(host = os.getenv("HOST"), database = os.getenv("DATABASE"), user = os.getenv("USER"), password = os.getenv("PASSWORD"), cursor_factory= RealDictCursor)
        print("Database connection was successful")
        return conn
      except Exception as Error:
        print("Connecting to database failed")
        print(f"Error: {Error}")
        time.sleep(10)

  def get_conn(self):
    return self.conn

  def set_conn(self, conn):
    self.conn = conn

database = Database_connection()