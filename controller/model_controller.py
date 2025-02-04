import numpy as np
from PIL import Image
from models import models
from information.model_info import plant_info

def predict_image(img, plant_name):
    """
    Fungsi untuk melakukan prediksi penyakit tanaman secara fleksibel.
    """
    if plant_name not in models:
        return {"error": f"Model untuk {plant_name} tidak ditemukan"}

    model = models[plant_name]["model"]
    labels = models[plant_name]["labels"]

    # Ambil ukuran input dari model
    input_shape = model.input_shape[1:3]  # (height, width)
    channels = model.input_shape[3]       # Jumlah channel

    # Resize gambar
    img = img.resize(input_shape)

    # Konversi ke array dan normalisasi
    i = np.array(img) / 255.0  

    # Sesuaikan jumlah channel
    if len(i.shape) == 2:  
        i = np.expand_dims(i, axis=-1)  # Jika grayscale, tambahkan channel
    if i.shape[-1] != channels:
        i = np.repeat(i, channels, axis=-1)

    # Reshape ke format model
    i = i.reshape((1,) + input_shape + (channels,))

    # Lakukan prediksi
    pred = model.predict(i)
    pred_class = np.argmax(pred)
    confidence = float(pred[0][pred_class] * 100)
    result = labels[pred_class]

    # Ambil informasi penyakit tanaman
    info = plant_info.get(plant_name, {}).get(result, {"description": "Unknown", "solution": "No solution available"})

    return {
        "plant_name": plant_name,
        "prediction": result,
        "confidence": confidence,
        "description": info["description"],
        "solution": info["solution"]
    }
