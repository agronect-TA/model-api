import boto3
import os
import logging
import io
import time
from botocore.exceptions import NoCredentialsError
from flask import request, jsonify
from PIL import Image

# Load konfigurasi dari environment variables
SPACES_ACCESS_KEY = os.getenv("SPACES_ACCESS_KEY")
SPACES_SECRET_KEY = os.getenv("SPACES_SECRET_KEY")
SPACES_REGION = os.getenv("SPACES_REGION")
SPACES_BUCKET_NAME = os.getenv("SPACES_BUCKET_NAME")
SPACES_ENDPOINT = os.getenv("SPACES_ENDPOINT")

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def upload_to_spaces(file_bytes, file_name, content_type):
    """Mengunggah file ke DigitalOcean Spaces di folder Image_Predict_Upload dan mengembalikan URL publik."""
    try:
        s3_client = boto3.client(
            "s3",
            region_name=SPACES_REGION,
            endpoint_url=SPACES_ENDPOINT,
            aws_access_key_id=SPACES_ACCESS_KEY,
            aws_secret_access_key=SPACES_SECRET_KEY
        )

        # Tambahkan folder "Image_Predict_Upload/"
        folder_name = "Image_Predict_Upload"
        full_file_path = f"{folder_name}/{file_name}"  # Path lengkap di dalam Spaces

        s3_client.put_object(
            Bucket=SPACES_BUCKET_NAME,
            Key=full_file_path,
            Body=file_bytes,
            ContentType=content_type,
            ACL="public-read"  # Agar dapat diakses secara publik
        )

        return f"{SPACES_ENDPOINT}/{SPACES_BUCKET_NAME}/{full_file_path}"
    except NoCredentialsError:
        logging.error("Kredensial tidak ditemukan")
        return None
    except Exception as e:
        logging.error(f"Error saat mengunggah ke Spaces: {e}")
        return None

def upload_middleware(f):
    """Middleware Flask untuk menangani upload gambar ke DigitalOcean Spaces."""
    def wrapper(*args, **kwargs):
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        try:
            # Baca gambar
            image_bytes = file.read()
            img = Image.open(io.BytesIO(image_bytes))

            # Tentukan nama file unik dalam folder "Image_Predict_Upload/"
            timestamp = int(time.time())
            file_name = f"{request.user_id}_{timestamp}.jpg"

            # Unggah ke DigitalOcean Spaces
            image_url = upload_to_spaces(image_bytes, file_name, file.content_type)

            if not image_url:
                return jsonify({"error": "Gagal mengunggah gambar"}), 500

            # Tambahkan URL gambar ke request agar bisa digunakan di route
            request.image_url = image_url
            request.image = img  # Gambar dalam format PIL (jika perlu)
        
        except Exception as e:
            logging.error(f"Error saat membaca file: {e}")
            return jsonify({"error": "File tidak valid"}), 400

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper
