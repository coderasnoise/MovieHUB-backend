from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime,timedelta


def generate_password_hash(password):
    return generate_password_hash(password)


def check_password(password, password_hash):
    return check_password_hash(password_hash, password)


SECRET_KEY = 'supersecretkey'


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token süresi doldu
    except jwt.InvalidTokenError:
        return None  # Geçersiz token