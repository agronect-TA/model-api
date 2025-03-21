from keras.api.models import load_model
import os

models = {
    "corn": {
        "path": "models/corn_model.h5",
        "labels": ["Corn Healthy", "Corn Gray Leaf Spot", "Corn Common Rust", "Corn Northern Leaf Blight"]
    },
    "rice": {
        "path": "models/rice_model.h5",
        "labels": ['Brown Spot', 'Healthy', 'Leaf Blast', 'Neck Blast']
    },
    "cassava": {
        "path": "models/cassava_model.h5",
        "labels": ['Cassava Bacterial Blight', 'Cassava Brown Streak Disease', 'Cassava Green Mottle', 'Cassava Mosaic Disease', 'Healthy']
    },
    "potato": {
        "path": "models/potato_model.h5",
        "labels": ['Early Blight', 'Healthy', 'Late Blight']
    }
    # Model lain bisa ditambahkan di sini nantinya
}

# Load semua model ke dalam dictionary
for plant, data in models.items():
    data["model"] = load_model(data["path"])