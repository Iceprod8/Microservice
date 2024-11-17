from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Movie
from ..schemas import MovieSchema

movie_blueprint = Blueprint("movies", __name__)
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movie_blueprint.route("/add", methods=["POST"])
def add_movie():
    data = request.get_json()
    errors = movie_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    try:
        new_movie = Movie(
            title=data['title'],
            genre_id=data['genre_id'],
            director=data.get('director'),
            release_date=data.get('release_date'),
            synopsis=data.get('synopsis'),
            duration=data.get('duration'),
            cast=data.get('cast'),
            rating=data.get('rating', 0)
        )
        db.session.add(new_movie)
        db.session.commit()
        return jsonify({"message": "Movie added successfully!", "movie": movie_schema.dump(new_movie)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@movie_blueprint.route("/all", methods=["GET"])
def get_movies():
    try:
        movies = Movie.query.all()
        return jsonify(movies_schema.dump(movies))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movie_blueprint.route("/<int:id>", methods=["GET"])
def get_movie(id):
    try:
        movie = Movie.query.get(id)
        if movie:
            return jsonify(movie_schema.dump(movie))
        else:
            return jsonify({"error": "Movie not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movie_blueprint.route("/<int:id>", methods=["PUT"])
def update_movie(id):
    data = request.get_json()
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    
    errors = movie_schema.validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    
    try:
        movie.title = data.get('title', movie.title)
        movie.genre = data.get('genre', movie.genre)
        movie.director = data.get('director', movie.director)
        movie.release_date = data.get('release_date', movie.release_date)
        movie.synopsis = data.get('synopsis', movie.synopsis)
        movie.duration = data.get('duration', movie.duration)
        movie.cast = data.get('cast', movie.cast)
        movie.rating = data.get('rating', movie.rating)
        db.session.commit()
        return jsonify({"message": "Movie updated successfully!", "movie": movie_schema.dump(movie)})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@movie_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_movie(id):
    try:
        movie = Movie.query.get(id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return jsonify({"message": "Movie deleted successfully!"})
        else:
            return jsonify({"error": "Movie not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
