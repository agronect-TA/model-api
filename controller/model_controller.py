import numpy as np
from models.models_loader import models
from information.model_info import plant_info

def predict_image(img, plant_name):
    model = models.get(plant_name, {}).get("model")
    labels = models.get(plant_name, {}).get("labels")

    if not model or not labels:
        return {"error": "Model not found for the given plant name"}

    # Debugging: Cek daftar label yang digunakan
    print(f"[DEBUG] Labels for {plant_name}: {labels}")

    # Ambil ukuran input dari model
    input_shape = model.input_shape[1:3]
    channels = model.input_shape[3]

    # Resize gambar
    img = img.resize(input_shape)

    # Konversi ke array dan normalisasi
    i = np.array(img) / 255.0  

    # Sesuaikan jumlah channel
    if len(i.shape) == 2:  
        i = np.expand_dims(i, axis=-1)
    if i.shape[-1] != channels:
        i = np.repeat(i, channels, axis=-1)

    # Reshape ke format model
    i = i.reshape((1,) + input_shape + (channels,))

    # Lakukan prediksi
    pred = model.predict(i)
    # Debugging: Lihat hasil prediksi
    print(f"[DEBUG] Prediksi mentah: {pred}")
    print(f"[DEBUG] Jumlah kelas di prediksi: {len(pred[0])}")
    print(f"[DEBUG] Jumlah label: {len(labels)}")

    # Validasi jumlah kelas dan label
# Debugging: Cek semua probabilitas prediksi dan indeksnya
    for idx, prob in enumerate(pred[0]):
        print(f"[DEBUG] Kelas ke-{idx}: Probabilitas {prob:.4f}")

    # Cek apakah model punya info tentang kelas
    if hasattr(model, 'class_indices'):
        print(f"[DEBUG] Class indices dari model: {model.class_indices}")
    if hasattr(model, 'classes_'):
        print(f"[DEBUG] Classes dari model: {model.classes_}")

    # Cari kelas dengan probabilitas tertinggi
    pred_class = np.argmax(pred)

    confidence = float(pred[0][pred_class] * 100)
    result = labels[pred_class]  # Ambil label berdasarkan indeks prediksi

    # Debugging: Cek apakah prediksi sesuai dengan label
    print(f"[DEBUG] Raw Prediction Output: {pred}")
    print(f"[DEBUG] Predicted Class Index: {pred_class}")
    print(f"[DEBUG] Predicted Class Label: {result}")

    # Ambil informasi penyakit tanaman
    plant_data = plant_info.get(plant_name, {})
    diseases = plant_data.get("diseases", {})

    # Normalisasi key agar cocok
    normalized_labels = {k.lower().strip(): v for k, v in diseases.items()}
    result_lower = result.lower().strip()

    # Debugging: Cek apakah informasi ditemukan
    print(f"[DEBUG] Available Disease Keys: {list(normalized_labels.keys())}")
    print(f"[DEBUG] Looking for Key: {result_lower}")

    info = normalized_labels.get(result_lower, {"description": "Unknown", "solution": "No solution available"})

    return {
        "plant_name": plant_name,
        "prediction": result,
        "confidence": confidence,
        "description": info["description"],
        "solution": info["solution"]
    }
