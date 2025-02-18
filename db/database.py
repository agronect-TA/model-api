import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi database
DB_CONFIG = {
    "user": "root",
    "password": "baguskeren77",
    "database": "agronect_skripsi",
    "host": "localhost",
    "port": 3306,
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def save_prediction(user_id, plant_name, image_bytes, prediction, confidence, description, solution):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO predictions (user_id, plant_name, image, prediction, confidence, description, solution) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user_id, plant_name, image_bytes, prediction, confidence, description, solution),
        )
    connection.commit()
    connection.close()
