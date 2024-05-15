# content_service.py
import os

from flask import current_app
from werkzeug.utils import secure_filename
from models import Movie, Series, db
from sqlalchemy.exc import IntegrityError


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def create_movie(data):
    movie = Movie(title=data['title'], description=data['description'], release_date=data['release_date'],
                  duration=data['duration'])
    db.session.add(movie)
    db.session.commit()
    return movie


def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    return movie


def create_series(data):
    series = Series(title=data['title'], description=data['description'], release_date=data['release_date'])
    db.session.add(series)
    db.session.commit()
    return series


def get_series(series_id):
    series = Series.query.get(series_id)
    return series


def content_already_exists(title, _type):
    if _type == 'movie':
        return Movie.query.filter_by(title=title).first() is not None
    elif _type == 'series':
        return Series.query.filter_by(title=title).first() is not None


def upload_content(content_data, file):
    title = content_data['title']
    _type = content_data['type'].lower()

    if content_already_exists(title, _type):
        return {"message": "Content with this title already exists."}, 409

    try:
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if _type == 'movie':
            content = Movie(
                title=title,
                description=content_data['description'],
                release_date=content_data['release_date'],
                duration=content_data['duration'],
                thumbnail=filename
            )
        elif _type == 'series':
            content = Series(
                title=title,
                description=content_data['description'],
                release_date=content_data['release_date'],
                thumbnail=filename
            )
        else:
            return {"message": "Invalid content type provided."}, 400

        db.session.add(content)
        db.session.commit()
        return {"id": content.movie_id if _type == 'movie' else content.series_id, "title": content.title, "type": _type}, 201

    except IntegrityError:
        db.session.rollback()
        return {"message": "Content could not be created due to an integrity error."}, 500


def delete_content(content_id):
    # İçeriği sorgula
    content = Movie.query.get(content_id)
    if not content:
        content = Series.query.get(content_id)
        if not content:
            return {"message": "Content not found"}, 404  # İçerik bulunamadı

    # İçeriği veritabanından sil
    try:
        db.session.delete(content)
        db.session.commit()
        return {"message": "Content deleted successfully"}, 200  # Başarılı silme
    except Exception as e:
        db.session.rollback()
        return {"message": f"An error occurred: {str(e)}"}, 500  # Silme sırasında hata


def get_contents():
    contents = []
    movies = Movie.query.all()
    series = Series.query.all()
    for movie in movies:
        thumbnail_url = f'http://localhost:5000/static/thumbnails/{movie.thumbnail}' if movie.thumbnail else None
        contents.append(
            {
                "content_id": movie.movie_id,
                "title": movie.title,
                "type": "movie",
                "description": movie.description,
                "thumbnail": thumbnail_url
            }
        )
    for serie in series:
        thumbnail_url = f'http://localhost:5000/static/thumbnails/{serie.thumbnail}' if serie.thumbnail else None
        contents.append(
            {
                "content_id": serie.series_id,
                "title": serie.title,
                "type": "series",
                "description": serie.description,
                "thumbnail": thumbnail_url
            }
        )
    return contents


def get_content_by_id(content_id):
    movie = Movie.query.get(content_id)
    if movie:
        return {"content_id": movie.movie_id, "title": movie.title, "type": "movie", "description": movie.description}
    serie = Series.query.get(content_id)
    if serie:
        return {"content_id": serie.series_id, "title": serie.title, "type": "series", "description": serie.description}
    return None
