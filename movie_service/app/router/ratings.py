from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Rating, Movie
from ..schemas import RatingSchema

rating_blueprint = Blueprint("ratings", __name__)
rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)

@rating_blueprint.route("/<int:id>/rate", methods=["POST"])
def rate_movie(id):
    data = request.get_json()
    user_id = data.get("user_id")
    score = data.get("score")

    if not user_id or not score:
        return jsonify({"error": "User ID and score are required"}), 400
    if score < 1 or score > 5:
        return jsonify({"error": "Score must be between 1 and 5"}), 400

    movie = Movie.query.get(id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    existing_rating = Rating.query.filter_by(movie_id=id, user_id=user_id).first()
    if existing_rating:
        existing_rating.score = score
    else:
        new_rating = Rating(movie_id=id, user_id=user_id, score=score)
        db.session.add(new_rating)

    db.session.commit()
    update_movie_rating(movie)
    return jsonify({"message": "Rating submitted successfully!"})

def update_movie_rating(movie):
    ratings = Rating.query.filter_by(movie_id=movie.id).all()
    if ratings:
        average_rating = sum(rating.score for rating in ratings) / len(ratings)
        movie.rating = round(min(average_rating, 5), 2)
    else:
        movie.rating = 0
    db.session.commit()

@rating_blueprint.route("/users/<int:user_id>/rated_movies", methods=["GET"])
def get_rated_movies_by_user(user_id):
    user_ratings = Rating.query.filter_by(user_id=user_id).all()
    if not user_ratings:
        return jsonify([]), 200
    rated_movies = [
        {
            "movie_id": rating.movie.id,
            "title": rating.movie.title,
            "genre": rating.movie.genre.name if rating.movie.genre else None,
            "director": rating.movie.director,
            "release_date": rating.movie.release_date,
            "duration": rating.movie.duration,
            "synopsis": rating.movie.synopsis,
            "cast": rating.movie.cast,
            "average_rating": rating.movie.rating,
            "user_rating": rating.score
        }
        for rating in user_ratings
    ]
    
    return jsonify(rated_movies), 200
