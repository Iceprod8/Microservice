import requests
from flask import jsonify

def validate_movie(movie_id):
    """
    Vérifie si un film existe en appelant une API externe.
    Retourne un message d'erreur en cas d'absence.
    """
    response = requests.get(f"http://localhost:80/movies/{movie_id}")
    
    if response.status_code != 200:
        return False, jsonify({"message": "Le film n'existe pas dans le service externe"}), 404
    
    movie_data = response.json()
    
    if movie_data["id"] != movie_id:
        return False, jsonify({"message": "Les données du film ne correspondent pas"}), 400

    return True, movie_data

def validate_user(user_id):
    """
    Vérifie si un utilisateur existe en appelant une API externe de gestion des utilisateurs.
    Retourne un message d'erreur en cas d'absence.
    """
    response = requests.get(f"http://localhost:80/users/users/{user_id}")
    
    if response.status_code != 200:
        return False, jsonify({"message": "L'utilisateur n'existe pas dans le service externe"}), 404
    
    user_data = response.json()
    
    if user_data["id"] != user_id:
        return False, jsonify({"message": "Les données de l'utilisateur ne correspondent pas"}), 400

    return True, user_data