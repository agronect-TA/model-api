import pytest
import numpy as np
from unittest.mock import MagicMock
from PIL import Image
from controller.model_controller import predict_image

@pytest.fixture
def mock_model():
    model = MagicMock()
    model.input_shape = (None, 224, 224, 3)
    model.predict.return_value = np.array([[0.1, 0.2, 0.6]])
    return model

@pytest.fixture
def mock_labels():
    return ["Corn Healthy", "Corn Gray Leaf Spot", "Corn Common Rust", "Corn Northern Leaf Blight"]

@pytest.fixture
def mock_potato_model():
    model = MagicMock()
    model.input_shape = (None, 256, 256, 3)
    model.output_shape = (None, 3)
    model.predict.return_value = np.array([[0.1, 0.7, 0.2]])
    return model

@pytest.fixture
def mock_potato_labels():
    return ["Early Blight", "Healthy", "Late Blight"]

@pytest.fixture
def mock_models(monkeypatch, mock_model, mock_labels, mock_potato_model, mock_potato_labels):
    monkeypatch.setattr("models.models_loader.models", {
        "corn": {"model": mock_model, "labels": mock_labels},
        "potato": {"model": mock_potato_model, "labels": mock_potato_labels}
    })

def test_predict_image_valid_corn(mock_models):
    img = Image.new("RGB", (224, 224))
    result = predict_image(img, "corn")
    assert "prediction" in result
    assert result["prediction"] in ["Corn Healthy", "Corn Gray Leaf Spot", "Corn Common Rust", "Corn Northern Leaf Blight"]
    assert result["confidence"] > 0


def test_predict_image_valid_potato(mock_models):
    img = Image.new("RGB", (256, 256))
    result = predict_image(img, "potato")
    assert "prediction" in result
    assert result["prediction"] in ["Early Blight", "Healthy", "Late Blight"]
    assert result["confidence"] > 0


def test_predict_image_invalid_model():
    img = Image.new("RGB", (256, 256))
    result = predict_image(img, "invalid_plant")
    assert "error" in result
    assert result["error"] == "Model not found for the given plant name"
