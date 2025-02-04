import jwt
from functools import wraps
from flask import request, jsonify
import os

# Load secret from environment variables
JWT_SECRET = "baguskeren77"

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"message": "Harap autentikasi terlebih dahulu"}), 401
        
        token = auth_header.split(" ")[1]
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user_id = decoded['id']
            request.email = decoded['email']
            request.name = decoded['name']
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token Anda telah kedaluwarsa. Silakan coba lagi"}), 400
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token tidak valid atau kedaluwarsa"}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function