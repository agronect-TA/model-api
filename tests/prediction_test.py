import pytest
import numpy as np
from unittest.mock import MagicMock
from PIL import Image
from controller.model_controller import predict_image

@pytest.fixture
def mock_model():
    model = MagicMock()
    model.input_shape = (None, 224, 224, 3)  # Sesuaikan dengan ukuran model
    model.predict.return_value = np.array([[0.1, 0.2, 0.6, 0.1]])  # Contoh output prediksi
    return model

@pytest.fixture
def mock_labels():
    return ["Corn Healthy", "Corn Gray Leaf Spot", "Corn Common Rust", "Corn Northern Leaf Blight"]

@pytest.fixture
def mock_rice_labels():
    return ["Brown Spot", "Healthly", "Leaf Blast", "Neck Blast"]

@pytest.fixture
def mock_cassava_labels():
    return ["Cassava Bacterial Blight", "Cassava Brown Streak Disease", "Cassava Green Mottle", "Cassava Mosaic Disease", "Healthy"]

@pytest.fixture
def mock_models(monkeypatch, mock_model, mock_labels, mock_rice_labels, mock_cassava_labels):
    monkeypatch.setattr("models.models_loader.models", {
        "corn": {"model": mock_model, "labels": mock_labels},
        "rice": {"model": mock_model, "labels": mock_rice_labels},
        "cassava": {"model": mock_model, "labels": mock_cassava_labels}
    })

def test_predict_image_valid(mock_models):
    img = Image.new("RGB", (256, 256))  # Buat gambar dummy
    result = predict_image(img, "corn")
    
    assert "prediction" in result
    assert result["prediction"] == "Corn Healthy"
    assert result["confidence"] > 0

def test_predict_image_valid_rice(mock_models):
    img = Image.new("RGB", (256, 256))  # Buat gambar dummy
    result = predict_image(img, "rice")
    
    assert "prediction" in result
    assert result["prediction"] == "Leaf Blast"
    assert result["confidence"] > 0

def test_predict_image_valid_cassava(mock_models):
    img = Image.new("RGB", (256, 256))  # Buat gambar dummy
    result = predict_image(img, "cassava")
    
    assert "prediction" in result
    assert result["prediction"] == "Healthy"
    assert result["confidence"] > 0

def test_predict_image_invalid_model():
    img = Image.new("RGB", (256, 256))  # Buat gambar dummy
    result = predict_image(img, "invalid_plant")
    
    assert "error" in result
    assert result["error"] == "Model not found for the given plant name"
