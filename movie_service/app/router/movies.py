from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Movie
from ..schemas import MovieSchema

movie_blueprint = Blueprint("movies", __name__)

@movie_blueprint.route("/movies", methods=["POST"])
def add_movie():
    data = request.get_json()
    new_movie = Movie(
        title=data.get('title'),
        genre=data.get('genre'),
        director=data.get('director'),
        release_date=data.get('release_date'),
        synopsis=data.get('synopsis')
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({"message": "Movie added successfully!"}), 201

@movie_blueprint.route("/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    movies_list = [
        {"id": movie.id, "title": movie.title, "genre": movie.genre, "director": movie.director,
         "release_date": movie.release_date, "synopsis": movie.synopsis}
        for movie in movies
    ]
    return jsonify(movies_list)

@movie_blueprint.route("/movies/<int:id>", methods=["GET"])
def get_movie(id):
    movie = Movie.query.get(id)
    if movie:
        return jsonify({"id": movie.id, "title": movie.title, "genre": movie.genre,
                        "director": movie.director, "release_date": movie.release_date,
                        "synopsis": movie.synopsis})
    else:
        return jsonify({"error": "Movie not found"}), 404

@movie_blueprint.route("/movies/<int:id>", methods=["PUT"])
def update_movie(id):
    data = request.get_json()
    movie = Movie.query.get(id)
    if movie:
        movie.title = data.get('title', movie.title)
        movie.genre = data.get('genre', movie.genre)
        movie.director = data.get('director', movie.director)
        movie.release_date = data.get('release_date', movie.release_date)
        movie.synopsis = data.get('synopsis', movie.synopsis)
        db.session.commit()
        return jsonify({"message": "Movie updated successfully!"})
    else:
        return jsonify({"error": "Movie not found"}), 404

@movie_blueprint.route("/movies/<int:id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"message": "Movie deleted successfully!"})
    else:
        return jsonify({"error": "Movie not found"}), 404