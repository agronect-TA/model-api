from keras.api.models import load_model
import os

models = {
    "corn": {
        "path": "models/corn_model.h5",
        "labels": ["Corn Healthy", "Corn Gray Leaf Spot", "Corn Common Rust", "Corn Northern Leaf Blight"]
    },
    # Model lain bisa ditambahkan di sini nantinya
}

# Load semua model ke dalam dictionary
for plant, data in models.items():
    data["model"] = load_model(data["path"])