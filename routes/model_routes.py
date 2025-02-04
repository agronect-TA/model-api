from flask import Blueprint, request, jsonify
from controller.model_controller import predict_corn
import io
from PIL import Image
from db import get_db_connection
from middleware.authenticate_middleware import auth_required

predict_blueprint = Blueprint('predict', __name__)

def save_prediction_to_db(image_bytes, prediction, confidence, description, solution,user_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO predictions (image, prediction, confidence, description, solution,user_id) VALUES (%s, %s, %s, %s, %s, %s)',
            (image_bytes, prediction, confidence, description, solution,user_id)
        )
    connection.commit()
    connection.close()


@predict_blueprint.route('/predict/corn', methods=["GET", "POST"])
@auth_required
def predict_corn_route():
    file = request.files.get('file')
    if file is None or file.filename == "":
        return jsonify({"error": "no file input in request"})
    
    image_bytes = file.read()
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((150, 150), Image.NEAREST)
    prediction, confidence, description, solution, _ = predict_corn(img)
    user_id = request.user_id
    save_prediction_to_db(image_bytes, prediction, confidence, description, solution,user_id)
    return jsonify({
        "user_id" : user_id,
        "prediction": prediction, 
        "confidence": confidence,
        "description": description,
        "solution": solution,
    })
