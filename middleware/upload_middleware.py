import boto3
import os
import logging
import io
import time
import functools
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
    """Mengunggah file ke DigitalOcean Spaces dan mengembalikan URL publik."""
    try:
        s3_client = boto3.client(
            "s3",
            region_name=SPACES_REGION,
            endpoint_url=SPACES_ENDPOINT,
            aws_access_key_id=SPACES_ACCESS_KEY,
            aws_secret_access_key=SPACES_SECRET_KEY
        )

        # Path dalam Spaces
        folder_name = "Image_Predict_Upload"
        full_file_path = f"{folder_name}/{file_name}"

        s3_client.put_object(
            Bucket=SPACES_BUCKET_NAME,
            Key=full_file_path,
            Body=file_bytes,
            ContentType=content_type or "image/jpeg",
            ACL="public-read"
        )

        # URL Publik
        public_url = f"https://{SPACES_BUCKET_NAME}.{SPACES_REGION}.digitaloceanspaces.com/{full_file_path}"
        return public_url

    except NoCredentialsError:
        logging.error("Kredensial DigitalOcean Spaces tidak ditemukan")
        return None
    except Exception as e:
        logging.error(f"Error saat mengunggah ke Spaces: {e}")
        return None

def upload_middleware(f):
    """Middleware Flask untuk meng-handle upload gambar ke DigitalOcean Spaces."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        file = request.files.get("file")
        if not file:
            logging.warning("Tidak ada file yang diunggah dalam request")
            return jsonify({"error": "No file uploaded"}), 400

        try:
            # Baca gambar
            image_bytes = file.read()
            img = Image.open(io.BytesIO(image_bytes))

            # Validasi format gambar
            valid_formats = ["JPEG", "JPG", "PNG", "WEBP"]
            if img.format not in valid_formats:
                logging.warning(f"Format gambar tidak didukung: {img.format}")
                return jsonify({"error": "Format gambar tidak didukung"}), 400

            # Tentukan nama file unik
            timestamp = int(time.time())
            file_name = f"{request.user_id}_{timestamp}.jpg"

            # Unggah ke DigitalOcean Spaces
            image_url = upload_to_spaces(image_bytes, file_name, file.content_type or "image/jpeg")

            if not image_url:
                logging.error(f"Gagal mengunggah gambar {file_name} ke DigitalOcean Spaces")
                return jsonify({"error": "Gagal mengunggah gambar"}), 500

            # Tambahkan URL gambar ke request agar bisa digunakan di route
            request.image_url = image_url
            request.image = img  # Gambar dalam format PIL jika diperlukan

        except Exception as e:
            logging.error(f"Error saat membaca file: {e}")
            return jsonify({"error": "File tidak valid"}), 400

        return f(*args, **kwargs)

    return wrapper
