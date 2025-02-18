from flask import Blueprint, request, jsonify
from controller.model_controller import predict_image
from db.database import save_prediction
from middleware.authenticate_middleware import auth_required
import io
from PIL import Image

predict_blueprint = Blueprint("predict", __name__)

@predict_blueprint.route("/predict/<plant_name>", methods=["POST"])
@auth_required
def predict_route(plant_name):
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Baca gambar
    image_bytes = file.read()
    img = Image.open(io.BytesIO(image_bytes))

    # Lakukan prediksi
    result = predict_image(img, plant_name)

    if "error" in result:
        return jsonify(result), 400

    # Simpan hasil ke database
    save_prediction(
        user_id=request.user_id,
        plant_name=plant_name,
        image_bytes=image_bytes,
        prediction=result["prediction"],
        confidence=result["confidence"],
        description=result["description"],
        solution=result["solution"],
    )

    return jsonify(result)
