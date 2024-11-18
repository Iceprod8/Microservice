from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Recommendation
from ..schemas import RecommendationSchema
import random

recommendations_blueprint = Blueprint("recommendations", __name__)
recommendation_schema = RecommendationSchema()
recommendation_schema = RecommendationSchema(many=True)

BASE_URL = "http://localhost:80"

# films favoris (limit 50)
MoviesFavList = {
    "1": {
        "id": 1,
        "title": "Inception",
        "genre": "Science Fiction",
        "director": "Christopher Nolan",
        "release_date": "2010-07-16",
        "duration": 148,
        "synopsis": "A thief who enters people's dreams to steal secrets is given a chance to erase his past crimes.",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
        "rating": 8.8
    },
    "2": {
        "id": 2,
        "title": "The Shawshank Redemption",
        "genre": "Drama",
        "director": "Frank Darabont",
        "release_date": "1994-09-22",
        "duration": 142,
        "synopsis": "Two imprisoned men bond over years, finding solace and eventual redemption through acts of common decency.",
        "cast": ["Tim Robbins", "Morgan Freeman"],
        "rating": 9.3
    },
    "3": {
        "id": 3,
        "title": "Interstellar",
        "genre": "Science Fiction",
        "director": "Christopher Nolan",
        "release_date": "2014-11-07",
        "duration": 169,
        "synopsis": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "rating": 8.6
    },
    "4": {
        "id": 4,
        "title": "Pulp Fiction",
        "genre": "Crime",
        "director": "Quentin Tarantino",
        "release_date": "1994-10-14",
        "duration": 154,
        "synopsis": "The lives of two mob hitmen, a boxer, a gangster's wife, and a diner bandit intertwine in four tales.",
        "cast": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
        "rating": 8.9
    }
}

# films les mieux notés (limit 50)
MovieBestRating = {
    "1": {
        "id": 1,
        "title": "The Godfather",
        "genre": "Crime",
        "director": "Francis Ford Coppola",
        "release_date": "1972-03-24",
        "duration": 175,
        "synopsis": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son.",
        "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
        "rating": 9.2
    },
    "2": {
        "id": 2,
        "title": "The Dark Knight",
        "genre": "Action",
        "director": "Christopher Nolan",
        "release_date": "2008-07-18",
        "duration": 152,
        "synopsis": "Batman faces his toughest test when he goes up against the Joker, a criminal mastermind.",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "rating": 9.0
    },
    "3": {
        "id": 3,
        "title": "Schindler's List",
        "genre": "Drama",
        "director": "Steven Spielberg",
        "release_date": "1993-11-30",
        "duration": 195,
        "synopsis": "In German-occupied Poland, industrialist Oskar Schindler saves his Jewish employees during the Holocaust.",
        "cast": ["Liam Neeson", "Ralph Fiennes", "Ben Kingsley"],
        "rating": 8.9
    },
    "4": {
        "id": 4,
        "title": "The Lord of the Rings: The Return of the King",
        "genre": "Adventure",
        "director": "Peter Jackson",
        "release_date": "2003-12-17",
        "duration": 201,
        "synopsis": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam.",
        "cast": ["Elijah Wood", "Viggo Mortensen", "Ian McKellen"],
        "rating": 8.9
    }
}

# films les mieux notés par l'user (limit 50)
MovieUserRating = {
    "1": {
        "id": 1,
        "title": "Forrest Gump",
        "genre": "Drama",
        "director": "Robert Zemeckis",
        "release_date": "1994-07-06",
        "duration": 142,
        "synopsis": "The story of a slow-witted but kind-hearted man from Alabama who witnesses and influences several historical events.",
        "cast": ["Tom Hanks", "Robin Wright", "Gary Sinise"],
        "rating": 8.8
    },
    "2": {
        "id": 2,
        "title": "Fight Club",
        "genre": "Drama",
        "director": "David Fincher",
        "release_date": "1999-10-15",
        "duration": 139,
        "synopsis": "An insomniac office worker and a devil-may-care soap maker form an underground fight club.",
        "cast": ["Brad Pitt", "Edward Norton", "Helena Bonham Carter"],
        "rating": 8.8
    },
    "3": {
        "id": 3,
        "title": "The Green Mile",
        "genre": "Drama",
        "director": "Frank Darabont",
        "release_date": "1999-12-10",
        "duration": 189,
        "synopsis": "The lives of guards on Death Row are affected by one of their charges, a black man accused of child murder and rape.",
        "cast": ["Tom Hanks", "Michael Clarke Duncan", "David Morse"],
        "rating": 8.6
    },
    "4": {
            "id": 4,
            "title": "The Silence of the Lambs",
            "genre": "Thriller",
            "director": "Jonathan Demme",
            "release_date": "1991-02-14",
            "duration": 118,
            "synopsis": "A young F.B.I. cadet must confide in an incarcerated and manipulative killer to catch another serial killer.",
            "cast": ["Jodie Foster", "Anthony Hopkins", "Lawrence A. Bonney"],
            "rating": 8.6
        }
}

# genres de films préférés de l'user
GenreMoviePreferenceUser = {
    "1": {
        "id": 1,
        "id_user": 101,
        "id_genre": "Action"
    },
    "2": {
        "id": 2,
        "id_user": 101,
        "id_genre": "Science Fiction"
    },
    "3": {
        "id": 3,
        "id_user": 101,
        "id_genre": "Drama"
    },
    "4": {
        "id": 4,
        "id_user": 101,
        "id_genre": "Crime"
    },
    "5": {
        "id": 5,
        "id_user": 101,
        "id_genre": "Comedy"
    }
}

@recommendations_blueprint.route("/<int:user_id>/", methods=["GET"])
def get_recommendations(user_id):
    try:
        movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen = get_all_datas(user_id)
        recommendations = generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen)
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def getListFavoris():
    url = f"{BASE_URL}/{id_list}/movies/recommendations" #remplacer id_list par l'id de la liste favoris dans la table list
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def getUserRatingMovies(user_id):
    url = f"{BASE_URL}/users/{user_id}/rated_movies"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def getPopularMovies():
    url = f"{BASE_URL}/movies/popular"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def getPreferredGenres():
    url = f"{BASE_URL}/genres"
    response = requests.get(url)
    if response.status_code == 200:
        return response.preferred_genres.json()
    return []

def getAlreadySeenMovies():
    url = f"{BASE_URL}/{id_list}/movies/recommendations" #remplacer id_list par l'id de la liste Deja vu dans la table list
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def get_all_datas(user_id):
    movies_fav_list = getListFavoris()
    movie_best_rating = getPopularMovies()
    movie_user_rating = getUserRatingMovies(user_id)
    preferred_genres = getPreferredGenres()
    movies_already_seen = getAlreadySeenMovies()
    return movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen

def generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen):
    recommendations = []

    #recuperer les realisateurs des films dans la liste de favoris, et des films bien notés par l'user
    directors_user_rating = [movie["director"] for movie in movie_user_rating]
    directors_fav_movies = [movie["director"] for movie in movies_fav_list]
    all_directors = directors_user_rating + directors_fav_movies
    unique_directors = list(set(all_directors))

    best_movies_for_genres_users = [movie for movie in movie_best_rating if movie["genre"] in preferred_genres]
    best_movies_for_directors_users = [movie for movie in movie_best_rating if movie["directors"] in unique_directors]

    # récuperer tous les films et supprimer ceux déjà vu
    all_movies = best_movies_for_genres_users + best_movies_for_directors_users
    recommendations = [movie for movie in all_movies if movie not in movies_already_seen]

    #melanger la liste pour en selectionner aleatoirement 10
    random.shuffle(recommendations)
    return recommendations[:10]
