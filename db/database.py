import pymysql
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Konfigurasi database
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
}

def get_db_connection():
    """Membuat koneksi ke database menggunakan konfigurasi dari environment variables."""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        logging.info(f"Koneksi ke database {DB_CONFIG['database']} di {DB_CONFIG['host']} berhasil.")
        return connection
    except pymysql.MySQLError as e:
        logging.error(f"Gagal konek ke database: {e}")
        return None

def save_prediction(user_id, plant_name, image_bytes, prediction, confidence, description, solution):
    """Menyimpan hasil prediksi ke dalam database."""
    connection = get_db_connection()
    if not connection:
        logging.error("Gagal menyimpan data karena koneksi database tidak tersedia.")
        return

    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO predictions (user_id, plant_name, image, prediction, confidence, description, solution)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, plant_name, image_bytes, prediction, confidence, description, solution))
        connection.commit()
        logging.info("Data prediksi berhasil disimpan.")
    except Exception as e:
        logging.error(f"Error saat menyimpan data: {e}")
    finally:
        connection.close()
        logging.info("Koneksi database ditutup.")