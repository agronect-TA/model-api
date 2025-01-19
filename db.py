import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_CONNECTION_NAME = os.getenv('DB_CONNECTION_NAME')

def get_db_connection():
    return pymysql.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        unix_socket=f'/cloudsql/{DB_CONNECTION_NAME}'
    )