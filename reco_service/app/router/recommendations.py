import requests
from flask import Blueprint, jsonify
from ..database import db
from ..models import Recommendation
from ..schemas import RecommendationSchema
import random

recommendations_blueprint = Blueprint("recommendations", __name__)
recommendation_schema = RecommendationSchema()
recommendation_schema = RecommendationSchema(many=True)

@recommendations_blueprint.route("/<int:user_id>/", methods=["GET"])
def get_recommendations(user_id):
    try:
        movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen = get_all_datas(user_id)
        recommendations = generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen)
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def getListFavoris():
    url = f"http://list_service:5000/lists/1/movies/recommendations"
    response = requests.get(url)
    if response.status_code == (200 | 201):
        print(response)
        return response.json()
    return []

def getUserRatingMovies(user_id):
    url = f"http://movie_service:5000/movies/users/{user_id}/rated_movies"
    response = requests.get(url)
    if response.status_code == (200 | 201):
        print(response)
        return response.json()
    return []

def getPopularMovies():
    url = f"http://movie_service:5000/movies/popular"
    response = requests.get(url)
    if response.status_code == (200 | 201):
        print(response)
        return response.json()
    return []

def getPreferredGenres(user_id):
    url = f"http://user_service:5000/users/{user_id}/preferences"
    response = requests.get(url)
    if response.status_code == (200 | 201):
        print(response)
        return response.preferred_genres.json()
    return []

def getAlreadySeenMovies():
    url = f"http://list_service:5000/lists/3/movies"
    response = requests.get(url)
    if response.status_code == (200 | 201):
        print(response)
        return response.json()
    return []

def get_all_datas(user_id):
    movies_fav_list = getListFavoris()
    movie_best_rating = getPopularMovies()
    movie_user_rating = getUserRatingMovies(user_id)
    preferred_genres = getPreferredGenres(user_id)
    movies_already_seen = getAlreadySeenMovies()
    return movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen

def generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen):
    recommendations = []

    directors_user_rating = [movie["director"] for movie in movie_user_rating]
    directors_fav_movies = [movie["director"] for movie in movies_fav_list]
    all_directors = directors_user_rating + directors_fav_movies
    unique_directors = list(set(all_directors))
    print(unique_directors)

    best_movies_for_genres_users = [movie for movie in movie_best_rating if movie["genre"] in preferred_genres]
    print(best_movies_for_genres_users)

    best_movies_for_directors_users = [movie for movie in movie_best_rating if movie["directors"] in unique_directors]
    print(best_movies_for_directors_users)

    all_movies = best_movies_for_genres_users + best_movies_for_directors_users
    print(all_movies)
    recommendations = [movie for movie in all_movies if movie not in movies_already_seen]
    print(recommendations)

    random.shuffle(recommendations)
    recommendations = recommendations[:10]
    for movie in recommendations:
        recommendation = Recommendation(
            id_movie=movie["id"],
            id_user=movie.get("user_id") 
        )
        db.session.add(recommendation)

    # Commit des changements dans la base de données
    db.session.commit()
    return recommendations
