import enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Role(enum.Enum):
    admin = "admin"
    user = "user"


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(512), nullable=False)
    favorites = db.relationship("Favorite", back_populates="user")
    role = db.Column(db.Enum('admin', 'user', name='user_roles'), default='user')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role.name if hasattr(self.role, 'name') else str(self.role)
        }



class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    # genre = db.Column(db.Text)
    description = db.Column(db.Text)
    release_date = db.Column(db.Text)
    duration = db.Column(db.Integer)
    thumbnail = db.Column(db.String(255))
    video_url = db.Column(db.String(255), nullable=True)


class Series(db.Model):
    __tablename__ = 'series'
    series_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    release_date = db.Column(db.Date)
    thumbnail = db.Column(db.String(255))
    video_url = db.Column(db.String(255), nullable=True)


class Episode(db.Model):
    __tablename__ = 'episodes'
    episode_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.series_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    episode_number = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    series = db.relationship("Series", back_populates="episodes")


class Favorite(db.Model):
    __tablename__ = 'favorites'
    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.Enum('movie', 'series'), nullable=False)
    user = db.relationship("User", back_populates="favorites")


# İlişkili tablolar için back_populate ayarları
Series.episodes = db.relationship("Episode", order_by=Episode.episode_id, back_populates="series")
User.favorites = db.relationship("Favorite", order_by=Favorite.favorite_id, back_populates="user")
