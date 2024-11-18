from .database import db

class Recommendation(db.Model):
    __tablename__ = "recommendation"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, nullable=False)
    id_movie = db.Column(db.Integer, nullable=False)