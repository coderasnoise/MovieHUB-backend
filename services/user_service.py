from models import User, db
from utils.security import generate_password_hash, check_password, generate_token


def register_user(data):
    password_hash = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash,
        role=data.get('admin', 'user')  # Varsayılan olarak 'user' atayabilirsiniz.
    )
    db.session.add(new_user)
    db.session.commit()
    return {"username": new_user.username, "email": new_user.email, "role": new_user.role}


def authenticate_user(credentials):
    user = User.query.filter_by(username=credentials['username']).first()
    if user and check_password(credentials['password'], user.password_hash):
        return generate_token(user.user_id)
    return None
