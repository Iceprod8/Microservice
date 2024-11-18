from flask import Blueprint, request, jsonify
from ..database import db
from ..models import UserList,ListType
from ..schemas import UserListSchema,ListTypeSchema
from ..validators import validate_movie, validate_user

list_blueprint = Blueprint("lists", __name__)
user_list_schema = UserListSchema()
user_lists_schema = UserListSchema(many=True)

@list_blueprint.route("/users/<int:id_user>/<int:id_movie>/<int:id_list>", methods=["POST"])
def add_movie_list(id_user, id_movie, id_list):
    # Valider l'existence de l'utilisateur
    is_valid_user, user_data = validate_user(id_user)
    if not is_valid_user:
        return jsonify(user_data), 404
    
    # Valider l'existence du film
    is_valid_movie, movie_data = validate_movie(id_movie)
    if not is_valid_movie:
        return jsonify(movie_data), 404

    # Vérifier si le type de liste existe
    list_type = ListType.query.get(id_list)
    if not list_type:
        return jsonify({"message": "Type de liste invalide"}), 400

    # Vérifier si l'utilisateur a déjà ajouté ce film dans cette liste
    existing_entry = UserList.query.filter_by(id_user=id_user, id_movie=id_movie, id_list_type=id_list).first()
    if existing_entry:
        return jsonify({"message": "Le film est déjà présent dans cette liste"}), 400

    # Créer une nouvelle entrée dans la liste
    new_list = UserList(
        id_user=id_user,
        first_name=user_data.get("first_name", ""),
        last_name=user_data.get("last_name", ""),
        email=user_data.get("email", ""),
        id_list_type=list_type.id,
        id_movie=movie_data.get("id"),
        name_movie=movie_data.get("title", "")
    )

    db.session.add(new_list)
    db.session.commit()

    user_list_data = user_list_schema.dump(new_list)
    return jsonify(user_list_data), 201

# Route pour obtenir tous les films d'une liste
@list_blueprint.route("/<int:id_list>/movies", methods=["GET"])
def get_list_movies(id_list):
    movies = UserList.query.filter_by(id_list_type=id_list).all()
    if not movies:
        return jsonify({"message": "list not found"}), 404
    result = UserListSchema.dump(movies)
    return jsonify(result), 200

# Route pour supprimer un film d'une liste
@list_blueprint.route("/<int:list_id>/movies/<int:id_movie>", methods=["DELETE"])
def delete_movie_from_list(list_id, id_movie):
    movie = UserList.query.filter_by(id_list_type=list_id, id_movie=id_movie).first()
    if not movie:
        return jsonify({"message": "Movie not found in list"}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie removed from list"}), 200

# Route pour supprimer une liste d'un utilisateur
@list_blueprint.route("/<int:list_id>/users/<int:user_id>", methods=["DELETE"])
def delete_list(user_id, list_id):
    user_list = UserList.query.filter_by(id_list_type=list_id, id_user=user_id).first()
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
