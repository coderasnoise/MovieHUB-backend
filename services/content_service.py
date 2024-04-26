# content_service.py
from models import Movie, Series, db


def create_movie(data):
    movie = Movie(title=data['title'], description=data['description'], release_date=data['release_date'], duration=data['duration'])
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


def upload_content(content_data):
    if content_data['type'] == 'movie':
        content = Movie(title=content_data['title'], description=content_data['description'])
    elif content_data['type'] == 'series':
        content = Series(title=content_data['title'], description=content_data['description'])

    db.session.add(content)
    db.session.commit()
    return {"title": content.title, "type": content_data['type']}


def get_contents():
    contents = []
    movies = Movie.query.all()
    series = Series.query.all()
    for movie in movies:
        contents.append({"content_id": movie.movie_id, "title": movie.title, "type": "movie"})
    for serie in series:
        contents.append({"content_id": serie.series_id, "title": serie.title, "type": "series"})
    return contents


def get_content_by_id(content_id):
    movie = Movie.query.get(content_id)
    if movie:
        return {"content_id": movie.movie_id, "title": movie.title, "type": "movie"}
    serie = Series.query.get(content_id)
    if serie:
        return {"content_id": serie.series_id, "title": serie.title, "type": "series"}
    return None
