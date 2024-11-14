from datetime import date
from database import db  # Importer db depuis database.py

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50))
    release_date = db.Column(db.Date, default=date.today)
    synopsis = db.Column(db.Text)

    def __repr__(self):
        return f"<Movie {self.title}>"
