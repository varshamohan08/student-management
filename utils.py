import psycopg2
from config import Config
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
import bcrypt

SECRET_KEY = "password"


def connect():
    return psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )

def generate_jwt_token(user_id, user_type):
    payload = {
        "user_id": user_id,
        "user_type": user_type,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # import pdb;pdb.set_trace()
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"error": "Token is missing!"}), 403
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
            user_type = payload["user_type"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated_function


def generate_bcrypt_hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_bcrypt_hash(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))