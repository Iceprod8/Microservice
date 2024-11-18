import requests
from flask import jsonify

def validate_movie(movie_id):
    response = requests.get(f"http://movie_service:5000/movies/{movie_id}")
    
    if response.status_code != 200:
        return False, {"message": "Le film n'existe pas dans le service externe"}
    
    movie_data = response.json()
    
    if movie_data["id"] != movie_id:
        return False, {"message": "Les données du film ne correspondent pas"}
    
    return True, movie_data


def validate_user(user_id):
    response = requests.get(f"http://user_service:5000/users/{user_id}")
    
    if response.status_code != 200:
        return False, {"message": "L'utilisateur n'existe pas dans le service externe"}
    
    user_data = response.json()
    
    if user_data["uid"] != user_id:
        return False, {"message": "Les données de l'utilisateur ne correspondent pas"}
    
    return True, user_data
