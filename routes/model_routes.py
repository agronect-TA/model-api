from flask import Blueprint, request, jsonify
from controller.model_controller import predict_image
from db.database import save_prediction
from middleware.authenticate_middleware import auth_required
from middleware.upload_middleware import upload_middleware

predict_blueprint = Blueprint("predict", __name__)

@predict_blueprint.route("/predict/<plant_name>", methods=["POST"])
@auth_required
@upload_middleware
def predict_route(plant_name):
    # Ambil gambar yang sudah diunggah (middleware sudah menangani upload)
    image_url = request.image_url
    img = request.image  # Gambar dalam format PIL (jika perlu)

    # Lakukan prediksi
    result = predict_image(img, plant_name)

    if "error" in result:
        return jsonify(result), 400

    # Simpan hasil ke database dengan URL gambar
    save_prediction(
        user_id=request.user_id,
        plant_name=plant_name,
        image_url=image_url,
        prediction=result["prediction"],
        confidence=result["confidence"],
        description=result["description"],
        solution=result["solution"],
    )

    # Tambahkan URL gambar ke response
    result["image_url"] = image_url

    return jsonify(result), 200
