import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

# Configure database connection
DB_USER = "root"
DB_PASSWORD = "baguskeren77"
DB_NAME = "agronect_skripsi"
DB_HOST = "localhost"  # Default to 'localhost' if not set
DB_PORT =3306  # Default MySQL port is 3306

def get_db_connection():
    return pymysql.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )