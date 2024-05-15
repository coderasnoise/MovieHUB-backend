from flask import request, jsonify, send_from_directory

from models import User, db, Movie
from services.content_service import create_movie, get_movie, create_series, get_series
from services.user_service import register_user, authenticate_user
from services.content_service import upload_content, get_contents, get_content_by_id
from services.favorite_service import add_to_favorites, get_favorites, remove_from_favorites
from utils.security import decode_token
from functools import wraps


# token kontrolü
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            user_id = decode_token(token)
            if not user_id:
                raise Exception('Invalid or expired token.')
        except:
            return jsonify({'message': 'Token is invalid or expired!'}), 401

        kwargs['user_id'] = user_id  # Kullanıcı ID'sini kwargs'a ekleyin
        return f(*args, **kwargs)

    return decorated



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.query.get(user_id)
        if user is None or user.role != 'admin':
            return jsonify({'message': 'Admin privileges required'}), 403
        kwargs.pop('user_id', None)  # Remove user_id before calling the actual function
        return f(*args, **kwargs)
    return decorated_function


def user_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(" ")[1] if 'Authorization' in request.headers else None
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            user_id = decode_token(token)
        except:
            return jsonify({'message': 'Token is invalid or expired!'}), 401

        kwargs['user_id'] = user_id  # Kullanıcı ID'sini kwargs'a ekleyin
        return f(*args, **kwargs)

    return decorated_function



def configure_routes(app):
    @app.route('/admin/users', methods=['GET', 'POST'])
    @user_token_required
    @admin_required
    def manage_users(user_id=None):
        if request.method == 'POST':
            user_data = request.get_json()
            user = User(email=user_data['email'], username=user_data['username'], password_hash=user_data['password'],
                        role=user_data['role'])
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User added successfully'}), 201
            pass
        elif request.method == 'GET':
            users = User.query.all()
            users_list = [{
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            } for user in users]
            return jsonify(users_list), 200

    @app.route('/admin/contents', methods=['POST'])
    @user_token_required
    @admin_required
    def add_content_admin():
        if 'thumbnail' not in request.files:
            return jsonify({'message': 'No file part'}), 400
        file = request.files['thumbnail']
        content_data = request.form.to_dict()
        result, status = upload_content(content_data, file)
        return jsonify(result), status

    @app.route('/static/thumbnails/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/admin/contents', methods=['GET'])
    @token_required
    @admin_required
    def list_contents_admin():
        contents = get_contents()
        return jsonify(contents), 200

    @app.route('/admin/contents/<int:content_id>', methods=['DELETE'])
    @token_required
    @admin_required
    def delete_content_route(content_id):
        result, status = delete_content_logic(content_id)  # İş mantığı fonksiyonunu çağır
        return jsonify(result), status

    def delete_content_logic(content_id):
        content = Movie.query.get(content_id)
        if not content:
            return {"message": "Content not found"}, 404

        try:
            db.session.delete(content)
            db.session.commit()
            return {"message": "Content deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500

    @app.route('/admin/users/<int:user_id>', methods=['DELETE'])
    @user_token_required
    @admin_required
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200

    @app.route('/admin/users/<int:user_id>', methods=['PUT'])
    @token_required
    @admin_required
    def update_user_role(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user_data = request.get_json()
        user.role = user_data.get('role', user.role)
        db.session.commit()
        return jsonify({'message': 'User role updated successfully'}), 200

    # login register endpointler --start--
    @app.route('/register', methods=['POST'])
    def register():
        user_data = request.get_json()
        user = register_user(user_data)
        if user:
            return jsonify(user.to_dict()), 201
        else:
            return jsonify({'message': 'Registration failed'}), 400

    @app.route('/login', methods=['POST'])
    def login():
        credentials = request.json
        token = authenticate_user(credentials)
        if token:
            return jsonify({"token": token}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    # içerik yükleme start
    @app.route('/contents', methods=['POST'])
    @token_required
    def add_content():
        content_data = request.json
        content = upload_content(content_data)
        return jsonify(content), 201

    @app.route('/user/<int:user_id>', methods=['GET'])
    @token_required
    def get_user(user_id):
        # Kullanıcı bilgilerini getirme işlemleri
        user = User.query.get(user_id)
        if user:
            return jsonify({
                "user_id": user.user_id,
                "email": user.email,
                "name": user.username
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404

    @app.route('/user/<int:user_id>', methods=['PUT'])
    @token_required
    def update_user(user_id):
        user_data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Kullanıcı bilgilerini güncelleme
        user.email = user_data.get('email', user.email)
        user.username = user_data.get('name', user.username)

        db.session.commit()

        return jsonify({'message': 'User updated successfully'}), 200

    # Content Listeleme ve Detay Görüntüleme
    @app.route('/contents', methods=['GET'])
    @token_required
    def list_contents(user_id):
        contents = get_contents()
        return jsonify(contents), 200

    @app.route('/contents/<int:content_id>', methods=['GET'])
    @token_required
    def content_detail(content_id,user_id):
        content = get_content_by_id(content_id)
        if content:
            return jsonify(content), 200
        else:
            return jsonify({"message": "Content not found"}), 404

    # favorilere ekleme
    @app.route('/favorites', methods=['POST'])
    @token_required
    def add_favorite(user_id):
        user_id = request.json['user_id']
        content_id = request.json['content_id']
        content_type = request.json['content_type']
        result = add_to_favorites(user_id, content_id, content_type)
        return jsonify(result), 201

    # favorileri listeleme
    @app.route('/favorites/<int:user_id>', methods=['GET'])
    @token_required
    def list_favorites(user_id):
        favorites = get_favorites(user_id)
        return jsonify(favorites), 200

    # favorilerden kaldırma
    @app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
    @user_token_required
    def remove_favorite(user_id, favorite_id):
        result = remove_from_favorites(favorite_id)
        return jsonify(result), 200
