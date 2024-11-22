from datetime import date,datetime,timezone
from .database import db

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)
    director = db.Column(db.String(50))
    release_date = db.Column(db.Date, default=date.today)
    duration = db.Column(db.Integer)
    synopsis = db.Column(db.Text)
    cast = db.Column(db.Text)
    rating = db.Column(db.Float, default=0)
    genre = db.relationship("Genre", back_populates="movies")
    ratings = db.relationship("Rating", backref="movie", lazy="dynamic")

    def __repr__(self):
        return f"<Movie {self.title}>"
    
class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    movies = db.relationship("Movie", back_populates="genre")

    def __repr__(self):
        return f"<Genre {self.name}>"

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Rating Movie ID: {self.movie_id}, Score: {self.score}>"
