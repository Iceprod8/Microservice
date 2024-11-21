from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from ..database import db
from ..models import Movie, Rating
from ..schemas import MovieSchema
from ..publisher import publish_movie_created, publish_movie_deleted, publish_movie_updated

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
            cast=data.get('cast')
        )
        db.session.add(new_movie)
        db.session.commit()

        publish_movie_created(new_movie)

        return jsonify({"message": "Movie added successfully!", "movie": movie_schema.dump(new_movie)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@movie_blueprint.route("/all_recent_release", methods=["GET"])
def get_recent_release_movies():
    try:
        # Récupérer les 15 films les plus récents triés par date de réalisation
        movies = Movie.query.order_by(Movie.release_date.desc()).limit(15).all()
        return jsonify(movies_schema.dump(movies))
    except Exception as e:
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
    
@movie_blueprint.route("/movies-by-ids", methods=["POST"])
def get_movies_by_ids():
    try:
        ids = request.json.get("ids", [])
        movies = Movie.query.filter(Movie.id.in_(ids)).all()
        return jsonify(movies_schema.dump(movies))
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
        movie.genre_id = data.get('genre_id', movie.genre_id)
        movie.director = data.get('director', movie.director)
        movie.release_date = data.get('release_date', movie.release_date)
        movie.synopsis = data.get('synopsis', movie.synopsis)
        movie.duration = data.get('duration', movie.duration)
        movie.cast = data.get('cast', movie.cast)
        db.session.commit()
        
        publish_movie_updated(movie)
        
        return jsonify({"message": "Movie updated successfully!", "movie": movie_schema.dump(movie)})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@movie_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_movie(id):
    try:
        movie = Movie.query.get(id)
        if movie:
            ratings = Rating.query.filter_by(movie_id=id).all()
            for rating in ratings:
                db.session.delete(rating)
            db.session.commit()

            db.session.delete(movie)
            db.session.commit()

            publish_movie_deleted(id)

            return jsonify({"message": "Movie and associated ratings deleted successfully!"})
        else:
            return jsonify({"error": "Movie not found"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@movie_blueprint.route("/popular", methods=["GET"])
def get_popular_movie():
    try:
        # Récupérer les 15 films les plus récents triés par date de réalisation
        movies = Movie.query.order_by(Movie.rating.desc()).limit(50).all()
        return jsonify(movies_schema.dump(movies))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@movie_blueprint.route("/search", methods=["GET"])
def search_movie_by_title():
    try:
        # Obtenir le titre depuis les paramètres de requête
        title = request.args.get('title', '').strip()
        if not title:
            return jsonify({"error": "Title parameter is required"}), 400

        # Rechercher les films avec un titre contenant la chaîne (insensible à la casse)
        movies = Movie.query.filter(Movie.title.ilike(f"%{title}%")).all()

        if movies:
            return jsonify(movies_schema.dump(movies))
        else:
            return jsonify({"message": "No movies found with the given title"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
