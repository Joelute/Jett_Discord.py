import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os
load_dotenv()

while True:
    try:
        conn = psycopg2.connect(host = os.getenv("HOST"), database = os.getenv("DATABASE"), user = os.getenv("USER"), password = os.getenv("PASSWORD"), cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as Error:
        print("Connecting to database failed")
        print(f"Error: {Error}")
        time.sleep(2)

def get_cursor():
    return cursor,conn
                