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
        recommendations = generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen, user_id)
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def getListFavoris(user_id):
    url = f"http://list_service:5000/lists/feed-list/{user_id}/1/recommendations"
    response = requests.get(url)
    return response.json()

def getUserRatingMovies(user_id):
    url = f"http://movie_service:5000/movies/users/{user_id}/rated_movies"
    response = requests.get(url)
    return response.json()

def getPopularMovies():
    url = f"http://movie_service:5000/movies/popular"
    response = requests.get(url)
    return response.json()

def getPreferredGenres(user_id):
    url = f"http://user_service:5000/users/{user_id}/preferences"
    response = requests.get(url)
    return response.json()['preferred_genres']

def getAlreadySeenMovies(user_id):
    url = f"http://list_service:5000/lists/feed-list/{user_id}/3/recommendations"
    response = requests.get(url)
    return response.json()

def get_all_datas(user_id):
    movies_fav_list = getListFavoris(user_id)
    movie_best_rating = getPopularMovies()
    movie_user_rating = getUserRatingMovies(user_id)
    preferred_genres = getPreferredGenres(user_id)
    movies_already_seen = getAlreadySeenMovies(user_id)
    return movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen

def generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen, user_id):
    recommendations = []

    # recupère les réalisateurs des films que le user a bien noté ou a mis en fav
    directors_user_rating = [movie["director"] for movie in movie_user_rating]
    directors_fav_movies = [movie["director"] for movie in movies_fav_list]
    all_directors = directors_user_rating + directors_fav_movies
    unique_directors = list(set(all_directors))

    # recupère les films que l'user pourrait aimer en fonction du genre de film (parmis les films bien notés)
    best_movies_for_genres_users = [movie for movie in movie_best_rating if movie["genre"] in preferred_genres]

    # recupère les films que l'user pourrait aimer en fonction du genre de réalisateur (parmis les films bien notés)
    best_movies_for_directors_users = [movie for movie in movie_best_rating if movie["director"] in unique_directors]

    # fusionner les deux dict
    all_movies = best_movies_for_genres_users + best_movies_for_directors_users
    print("all_movies", all_movies)
    print("movies_already_seen", movies_already_seen)
    recommendations = all_movies
    # retirer les films que le user a deja vu
    if not movies_already_seen["message"] :
        recommendations = [movie for movie in all_movies if movie not in movies_already_seen]
    recommendations
    print("recommendations", recommendations)

    # melanger et en prendre que 10
    random.shuffle(recommendations)
    recommendations = recommendations[:10]

    # enregister les films en bdd
    for movie in recommendations:
        recommendation = Recommendation(
            id_movie=movie["id"],
            id_user=user_id
        )
        db.session.add(recommendation)
    db.session.commit()
    return recommendations
