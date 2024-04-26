from flask import request, jsonify
from services.content_service import create_movie, get_movie, create_series, get_series
from services.user_service import register_user, authenticate_user
from services.content_service import upload_content, get_contents, get_content_by_id
from services.favorite_service import add_to_favorites, get_favorites, remove_from_favorites


def configure_routes(app):
    # login register endpointler --start--
    @app.route('/register', methods=['POST'])
    def register():
        user_data = request.json
        user = register_user(user_data)
        return jsonify(user), 201

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
    def add_content():
        content_data = request.json
        content = upload_content(content_data)
        return jsonify(content), 201

    # Content Listeleme ve Detay Görüntüleme
    @app.route('/contents', methods=['GET'])
    def list_contents():
        contents = get_contents()
        return jsonify(contents), 200

    @app.route('/contents/<int:content_id>', methods=['GET'])
    def content_detail(content_id):
        content = get_content_by_id(content_id)
        if content:
            return jsonify(content), 200
        else:
            return jsonify({"message": "Content not found"}), 404

    # favorilere ekleme
    @app.route('/favorites', methods=['POST'])
    def add_favorite():
        user_id = request.json['user_id']
        content_id = request.json['content_id']
        content_type = request.json['content_type']
        result = add_to_favorites(user_id, content_id, content_type)
        return jsonify(result), 201

    # favorileri listeleme
    @app.route('/favorites/<int:user_id>', methods=['GET'])
    def list_favorites(user_id):
        favorites = get_favorites(user_id)
        return jsonify(favorites), 200

    # favorilerden kaldırma
    @app.route('/favorites', methods=['DELETE'])
    def remove_favorite():
        favorite_id = request.json['favorite_id']
        result = remove_from_favorites(favorite_id)
        return jsonify(result), 200





    @app.route('/movies', methods=['POST'])
    def add_movie():
        data = request.json
        movie = create_movie(data)
        return jsonify(movie), 201

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    def retrieve_movie(movie_id):
        movie = get_movie(movie_id)
        return jsonify(movie), 200

    @app.route('/series', methods=['POST'])
    def add_series():
        data = request.json
        series = create_series(data)
        return jsonify(series), 201

    @app.route('/series/<int:series_id>', methods=['GET'])
    def retrieve_series(series_id):
        series = get_series(series_id)
        return jsonify(series), 200
