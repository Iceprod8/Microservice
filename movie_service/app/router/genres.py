from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Genre
from ..schemas import GenreSchema

genre_blueprint = Blueprint("genres", __name__)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@genre_blueprint.route("/genres", methods=["POST"])
def add_genre():
    data = request.get_json()
    genre_name = data.get("name")
    if not genre_name:
        return jsonify({"error": "Genre name is required"}), 400

    genre = Genre(name=genre_name)
    db.session.add(genre)
    db.session.commit()
    return jsonify({"message": "Genre added successfully!"}), 201

@genre_blueprint.route("/genres", methods=["GET"])
def get_genres():
    genres = Genre.query.all()
    genres_list = [{"id": genre.id, "name": genre.name} for genre in genres]
    return jsonify(genres_list)
