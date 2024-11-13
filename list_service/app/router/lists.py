from flask import Blueprint, request, jsonify
from ..database import db
from ..models import UserList, ListMovie, ListType
from ..schemas import UserListSchema, ListMovieSchema, ListTypeSchema
from ..validators import validate_movie, validate_user

list_blueprint = Blueprint("lists", __name__)
user_list_schema = UserListSchema()
user_lists_schema = UserListSchema(many=True)
list_movie_schema = ListMovieSchema()
list_movies_schema = ListMovieSchema(many=True)

# Route pour créer une nouvelle liste pour un utilisateur
@list_blueprint.route("/users/<int:user_id>", methods=["POST"])
def create_list(user_id):
    # Valider l'existence de l'utilisateur
    is_valid_user, user_data = validate_user(user_id)
    if not is_valid_user:
        return user_data  # Retourne le message d'erreur si l'utilisateur n'existe pas
    
    data = request.get_json()
    list_type = ListType.query.filter_by(name_list=data["list_type"]).first()
    
    if not list_type:
        return jsonify({"message": "Invalid list type"}), 400
    
    new_list = UserList(
        id_user=user_id,
        id_list_type=list_type.id
    )
    db.session.add(new_list)
    db.session.commit()
    user_list_data = user_list_schema.dump(new_list)
    return jsonify(user_list_data), 201

# Route pour ajouter un film dans une liste d'un utilisateur
@list_blueprint.route("/<int:list_id>/movies", methods=["POST"])
def add_movie_to_list(list_id):
    data = request.get_json()
    movie_id = data["id_movie"]
    
    # Valider l'existence du film
    is_valid_movie, movie_data = validate_movie(movie_id)
    if not is_valid_movie:
        return movie_data  # Retourne le message d'erreur si le film n'existe pas

    new_movie = ListMovie(
        id_user_list=list_id,
        id_movie=movie_id
    )
    db.session.add(new_movie)
    db.session.commit()
    movie_data = list_movie_schema.dump(new_movie)
    return jsonify(movie_data), 201

# Route pour obtenir toutes les listes d'un utilisateur
@list_blueprint.route("/<int:user_id>/lists/", methods=["GET"])
def get_user_lists(user_id):
    user_lists = UserList.query.filter_by(id_user=user_id).all()
    result = user_lists_schema.dump(user_lists)
    return jsonify(result), 200

# Route pour obtenir tous les films d'une liste
@list_blueprint.route("/lists/<int:list_id>/movies", methods=["GET"])
def get_list_movies(list_id):
    movies = ListMovie.query.filter_by(id_user_list=list_id).all()
    result = list_movies_schema.dump(movies)
    return jsonify(result), 200

# Route pour supprimer un film d'une liste
@list_blueprint.route("/<int:list_id>/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie_from_list(list_id, movie_id):
    movie = ListMovie.query.filter_by(id_user_list=list_id, id_movie=movie_id).first()
    if not movie:
        return jsonify({"message": "Movie not found in list"}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie removed from list"}), 200

# Route pour supprimer une liste d'un utilisateur
@list_blueprint.route("/<int:list_id>/users/<int:user_id>", methods=["DELETE"])
def delete_list(user_id, list_id):
    user_list = UserList.query.filter_by(id=list_id, id_user=user_id).first()
    if not user_list:
        return jsonify({"message": "List not found"}), 404
    
    db.session.delete(user_list)
    db.session.commit()
    return jsonify({"message": "List deleted successfully"}), 200

# Schéma pour sérialiser les types de liste
list_type_schema = ListTypeSchema(many=True)

# Route pour obtenir tous les types de liste
@list_blueprint.route("/list-types", methods=["GET"])
def get_all_list_types():
    list_types = ListType.query.all()
    result = list_type_schema.dump(list_types)
    return jsonify(result), 200
