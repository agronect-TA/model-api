from flask import Flask
from routes.model_routes import predict_blueprint
import os

app = Flask(__name__)

# Register blueprint
app.register_blueprint(predict_blueprint)

@app.route("/")
def home():
    return "Disease Prediction API is running!"

if __name__ == "__main__":
    app.run(debug=True)
