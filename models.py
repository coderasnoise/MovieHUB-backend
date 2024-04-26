from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

db = SQLAlchemy()
Base = declarative_base()

# Veritabanı bağlantısını yapılandırma
engine = create_engine('mysql+pymysql://batug:pass@35.226.213.195:3306/moviehub')
Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(60), nullable=False)

class Movie(Base):
    __tablename__ = 'movies'
    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    release_date = Column(Date)
    duration = Column(Integer)

class Series(Base):
    __tablename__ = 'series'
    series_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    release_date = Column(Date)

class Episode(Base):
    __tablename__ = 'episodes'
    episode_id = Column(Integer, primary_key=True, autoincrement=True)
    series_id = Column(Integer, ForeignKey('series.series_id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    episode_number = Column(Integer)
    release_date = Column(Date)
    series = relationship("Series", back_populates="episodes")

class Favorite(Base):
    __tablename__ = 'favorites'
    favorite_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    content_id = Column(Integer, nullable=False)
    content_type = Column(Enum('movie', 'series'), nullable=False)

Series.episodes = relationship("Episode", order_by=Episode.episode_id, back_populates="series")
User.favorites = relationship("Favorite", order_by=Favorite.favorite_id, back_populates="user")


