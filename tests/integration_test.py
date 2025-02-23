import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:5000"
LOGIN_URL = "http://206.189.153.35:3000/signin"  # Ganti dengan URL API utama
PREDICT_CORN_URL = f"{BASE_URL}/predict/corn"
PREDICT_RICE_URL = f"{BASE_URL}/predict/rice"
PREDICT_CASSAVA_URL = f"{BASE_URL}/predict/cassava"
TEST_IMAGE_CORN_PATH = "tests/test_image_corn.JPG"
TEST_IMAGE_RICE_PATH = "tests/test_image_rice.jpg"
TEST_IMAGE_CASSAVA_PATH = "tests/test_image_cassava.jpg"

def get_access_token():
    """Login ke API utama untuk mendapatkan access_token."""
    response = requests.post(LOGIN_URL, json={
        "email": "sfqbs@gmail.com",
        "password": "Baguskeren77"
    })
    print(response.json()) 
    assert response.status_code == 200, "Gagal login, periksa kredensial."
    return response.json().get("access_token")

@pytest.fixture(scope="function")
def access_token():
    return get_access_token()

def test_predict_corn_success(access_token):
    """Mengirim gambar corn dan memastikan prediksi berhasil."""
    with open(TEST_IMAGE_CORN_PATH, "rb") as img:
        files = {"file": img}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(PREDICT_CORN_URL, files=files, headers=headers)
    
    assert response.status_code == 200, f"Gagal prediksi: {response.json()}"
    data = response.json()
    assert "prediction" in data, "Response tidak memiliki prediksi."
    assert "confidence" in data, "Response tidak memiliki tingkat keyakinan."

def test_predict_rice_success(access_token):
    """Mengirim gambar rice dan memastikan prediksi berhasil."""
    with open(TEST_IMAGE_RICE_PATH, "rb") as img:
        files = {"file": img}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(PREDICT_RICE_URL, files=files, headers=headers)
    
    assert response.status_code == 200, f"Gagal prediksi: {response.json()}"
    data = response.json()
    assert "prediction" in data, "Response tidak memiliki prediksi."
    assert "confidence" in data, "Response tidak memiliki tingkat keyakinan."

def test_predict_cassava_success(access_token):
    """Mengirim gambar cassava dan memastikan prediksi berhasil."""
    with open(TEST_IMAGE_CASSAVA_PATH, "rb") as img:
        files = {"file": img}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(PREDICT_CASSAVA_URL, files=files, headers=headers)
    
    assert response.status_code == 200, f"Gagal prediksi: {response.json()}"
    data = response.json()
    assert "prediction" in data, "Response tidak memiliki prediksi."
    assert "confidence" in data, "Response tidak memiliki tingkat keyakinan."

def test_predict_no_token():
    """Memastikan akses tanpa token ditolak."""
    with open(TEST_IMAGE_CORN_PATH, "rb") as img:
        files = {"file": img}
        response = requests.post(PREDICT_CORN_URL, files=files)
    
    assert response.status_code == 401, "Akses tanpa token seharusnya ditolak."

def test_predict_invalid_token():
    """Memastikan token tidak valid ditolak."""
    with open(TEST_IMAGE_CORN_PATH, "rb") as img:
        files = {"file": img}
        headers = {"Authorization": "Bearer invalid_token"}
        response = requests.post(PREDICT_CORN_URL, files=files, headers=headers)
    
    assert response.status_code == 403, "Token tidak valid seharusnya ditolak."
